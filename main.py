from argparse import ArgumentParser
import asyncio
from openai import AsyncOpenAI
from playwright.async_api import async_playwright
from logging import getLogger
from src.bot.survive_the_internet.survive_the_internet_repository import (
    SurviveTheInternetRepository,
)
from src.logging import configure_logging
from src.llm_service import LLMService
from src.bot.survive_the_internet.survive_the_internet_bot import SurviveTheInternetBot
from src.playwright import join_game
from src.settings import get_settings

configure_logging()
log = getLogger(__name__)


async def step_executor(coroutine, max_retries: int = 3):
    phase_name = coroutine.__name__
    for i in range(max_retries):
        attempt = i + 1
        try:
            log.info(
                f"Attempting queue task: {phase_name} (Attempt {attempt}/{max_retries})"
            )
            await coroutine()
            log.info(f"Task {phase_name} executed successfully.")
            return
        except Exception as e:
            log.error(f"Task {phase_name} failed on attempt {attempt}: {e}")
            if attempt == max_retries:
                log.critical(
                    f"Task {phase_name} exhausted all retries. Proceeding to next queue item."
                )
            await asyncio.sleep(2)


async def main():
    argument_parser = ArgumentParser()
    argument_parser.add_argument(
        "--room-code", required=True, help="The room code of the game to join."
    )
    args = argument_parser.parse_args()

    log.info("Initializing Playwright and browser context.")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await join_game(
            get_settings().bot_name, get_settings.join_url, args.room_code, context
        )
        repository = SurviveTheInternetRepository(page, 5 * 60 * 1000)

        client = AsyncOpenAI(
            base_url=get_settings().llm_base_url, api_key=get_settings().llm_api_key
        )
        llm_service = LLMService(client, get_settings().llm_model)

        try:
            bot = SurviveTheInternetBot(repository, llm_service)
        except Exception:
            log.critical("Bot failed to join game. Closing browser.")
            await browser.close()
            return

        for task_coroutine in bot.queue:
            await step_executor(task_coroutine)

        log.info("All queued tasks finished. Closing browser.")
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
