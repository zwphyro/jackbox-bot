import asyncio
from openai import AsyncOpenAI
from playwright.async_api import async_playwright
from logging import getLogger
from logger import configure_logging
from llm_service import LLMService
from bot_logic import SurviveTheInternetPhases

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


async def run_jackbox_bot(
    bot_name: str,
    room_code: str,
    openai_base_url: str,
    openai_api_key: str,
    openai_model: str,
):
    log.info("Initializing Playwright and browser context.")
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()

        client = AsyncOpenAI(base_url=openai_base_url, api_key=openai_api_key)

        phases = await SurviveTheInternetPhases.join_game(
            bot_name,
            "https://jackbox.fun/",
            room_code,
            context,
            5 * 60 * 1000,
            LLMService(client, openai_model),
        )

        queue = [
            phases.initial_response,
            phases.twist_response,
            phases.text_voting,
            phases.initial_response,
            phases.twist_response,
            phases.text_voting,
            phases.initial_response,
            phases.twist_response,
            phases.text_voting,
            phases.image_choice,
            phases.image_twist,
            phases.image_voting,
        ]

        log.info(f"Queue populated with {len(queue)} sequential tasks.")

        for task_coroutine in queue:
            await step_executor(task_coroutine)

        log.info("All queued tasks finished. Closing browser.")
        await browser.close()


if __name__ == "__main__":
    ROOM_CODE = "xmkm"
    BOT_NAME = "RoboJoke"
    OPENAI_BASE_URL = "https://router.huggingface.co/v1"
    OPENAI_API_KEY = ""
    OPENAI_MODEL = "openai/gpt-oss-20b:groq"

    asyncio.run(
        run_jackbox_bot(
            BOT_NAME, ROOM_CODE, OPENAI_BASE_URL, OPENAI_API_KEY, OPENAI_MODEL
        )
    )
