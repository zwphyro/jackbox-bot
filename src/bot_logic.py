from playwright.async_api import BrowserContext, Page
from llm_service import LLMService
from logging import getLogger

log = getLogger(__name__)


class SurviveTheInternetPhases:
    def __init__(self, page: Page, llm_service: LLMService, timeout: int):
        self._page = page
        self._llm_service = llm_service
        self._timeout = timeout

    @classmethod
    async def join_game(
        cls,
        name: str,
        url: str,
        room_code: str,
        context: BrowserContext,
        timeout: int,
        llm_service: LLMService,
    ):
        log.info("Joining game...")
        page = await context.new_page()
        await page.goto(url)
        await page.wait_for_selector("#roomcode")
        await page.fill("#roomcode", room_code)
        await page.fill("#username", name)
        await page.click("#button-join")
        log.info("Joined game.")

        return cls(page, llm_service, timeout)

    async def initial_response(self):
        log.info("Executing phase: Initial Response")
        question_locator = self._page.locator(".belowBlackBox")
        await question_locator.wait_for(state="visible", timeout=self._timeout)
        question_text = await question_locator.inner_text()

        payload = {"prompt_text": question_text}
        response = await self._llm_service.generate_initial_response(payload)

        await self._page.fill("#input-text-textarea", response)
        await self._page.click("#buttons > div > div > button")
        log.info("Initial Response phase completed.")

    async def twist_response(self):
        log.info("Executing phase: Twist Response")
        black_box = self._page.locator(".blackBox")
        await black_box.wait_for(state="visible", timeout=self._timeout)

        context_text = await black_box.inner_text()
        prompt_text = await self._page.locator(".belowBlackBox").inner_text()

        payload = {
            "context_text": context_text,
            "prompt_text": prompt_text,
        }
        answer = await self._llm_service.generate_twist_response(payload)

        await self._page.fill("#input-text-textarea", answer)
        await self._page.click("#buttons > div > div > button")
        log.info("Twist Response phase completed.")

    async def text_voting(self):
        log.info("Executing phase: Text Voting")
        choices_container = self._page.locator("#choicesRegion > div > *")
        await choices_container.first.wait_for(state="visible", timeout=self._timeout)

        options = await choices_container.all()
        choices_data = []
        for index, option in enumerate(options):
            choices_data.append(
                {
                    "index": index,
                    "header": await option.locator(".voteTwistHeader").inner_text(),
                    "player": await option.locator(".votePlayer").inner_text(),
                    "response": await option.locator(".voteResponse").inner_text(),
                }
            )

        payload = {"options": choices_data}
        selected_index = await self._llm_service.choose_text_vote(payload)

        if 0 <= selected_index < len(options):
            await options[selected_index].click()
            log.info(f"Clicked option {selected_index} for Text Voting.")
        else:
            await options[0].click()
            log.warning("Invalid index returned. Clicked option 0 fallback.")

    async def image_choice(self):
        log.info("Executing phase: Image Choice")
        question_locator = self._page.locator(".blackBox")
        await question_locator.wait_for(state="visible", timeout=self._timeout)
        question_text = await question_locator.inner_text()

        choices_container = self._page.locator("#choicesRegion > div > *")
        await choices_container.first.wait_for(state="visible", timeout=self._timeout)

        options = await choices_container.all()
        choices_data = []
        for index, option in enumerate(options):
            choices_data.append(
                {
                    "index": index,
                    "response": await option.locator("button").inner_text(),
                }
            )

        payload = {
            "question": question_text,
            "options": choices_data,
        }
        selected_index = await self._llm_service.choose_image_response(payload)

        if 0 <= selected_index < len(options):
            await options[selected_index].click()
            log.info(f"Clicked option {selected_index} for Image Choice.")
        else:
            await options[0].click()
            log.warning("Invalid index returned. Clicked option 0 fallback.")

    async def image_twist(self):
        log.info("Executing phase: Image Twist Comment")
        final_image = self._page.locator(".finalRoundImage")
        await final_image.wait_for(state="visible", timeout=self._timeout)

        image_description = await final_image.get_attribute("aria-label")
        prompt_text = await self._page.locator(".belowBlackBox").inner_text()

        payload = {
            "image_description": image_description,
            "prompt_text": prompt_text,
        }
        answer = await self._llm_service.generate_image_twist(payload)

        await self._page.fill("#input-text-textarea", answer)
        await self._page.click("#buttons > div > div > button")
        log.info("Image Twist phase completed.")

    async def image_voting(self):
        log.info("Executing phase: Image Voting")
        choices_container = self._page.locator("#choicesRegion > div > *")
        await choices_container.first.wait_for(state="visible", timeout=self._timeout)

        options = await choices_container.all()
        choices_data = []
        for index, option in enumerate(options):
            choices_data.append(
                {
                    "index": index,
                    "image_description": await option.locator(
                        ".voteThumbnail"
                    ).inner_text(),
                    "player": await option.locator(".votePlayer").inner_text(),
                    "response": await option.locator(".voteResponse").inner_text(),
                }
            )

        payload = {"options": choices_data}
        selected_index = await self._llm_service.choose_image_vote(payload)

        if 0 <= selected_index < len(options):
            await options[selected_index].click()
            log.info(f"Clicked option {selected_index} for Image Voting.")
        else:
            await options[0].click()
            log.warning("Invalid index returned. Clicked option 0 fallback.")
