import asyncio
from openai import AsyncOpenAI
from playwright.async_api import async_playwright
from logging import getLogger
from src.args import get_args
from src.enums import GamesEnum
from src.logging import setup_logging
from src.playwright import join_game
from src.games import setup_registry
from src.registry import GameRegistry
from src.settings import get_settings


log = getLogger(__name__)


async def main():
    settings = get_settings()
    args = get_args()

    setup_logging(settings.logging.level)
    setup_registry()

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
        client = AsyncOpenAI(
            base_url=settings.llm.base_url, api_key=settings.llm.api_key
        )

        game_entry = GameRegistry.get_game_entry(GamesEnum.SurviveTheInternet)

        repository = game_entry.repository(page, settings.playwright.timeout_ms)

        llm_proxy = game_entry.llm_proxy(
            client,
            settings.llm.model,
            game_entry.prompts,
        )

        try:
            bot = game_entry.bot(repository, llm_proxy)
        except Exception:
            log.critical("Bot failed to join game. Closing browser.")
            await browser.close()
            return

        await bot.run()

        log.info("All queued tasks finished. Closing browser.")
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
