import asyncio
from openai import AsyncOpenAI
from playwright.async_api import async_playwright
from logging import getLogger
from src.args import get_args
from src.games.survive_the_internet.repository import (
    SurviveTheInternetRepository,
)
from src.logging import setup_logging
from src.games.survive_the_internet.llm_proxy import SurviveTheInternetLLMProxy
from src.games.survive_the_internet.bot import SurviveTheInternetBot
from src.playwright import join_game
from src.prompts import get_prompts
from src.settings import get_settings


log = getLogger(__name__)


async def step_executor(coroutine, max_retries: int = 3):
    log = getLogger(__name__)

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
    settings = get_settings()
    prompts = get_prompts()
    args = get_args()

    setup_logging(settings.logging.level)

    log.info("Initializing Playwright and browser context.")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=not args.preview)
        context = await browser.new_context(user_agent=settings.playwright.user_agent)
        page = await join_game(
            settings.jackbox.bot_name,
            settings.jackbox.join_url,
            args.room_code,
            context,
        )
        repository = SurviveTheInternetRepository(page, settings.playwright.timeout_ms)

        client = AsyncOpenAI(
            base_url=settings.llm.base_url, api_key=settings.llm.api_key
        )
        llm_proxy = SurviveTheInternetLLMProxy(
            client,
            settings.llm.model,
            prompts.survive_the_internet,
        )

        try:
            bot = SurviveTheInternetBot(repository, llm_proxy)
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
