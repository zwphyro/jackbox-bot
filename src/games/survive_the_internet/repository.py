from logging import getLogger
from playwright.async_api import Page
from src.games.survive_the_internet.schemas import (
    ImageChoiceOption,
    ImageVotingOption,
    TextVotingOption,
)

log = getLogger(__name__)


class SurviveTheInternetRepository:
    def __init__(self, page: Page, timeout: int):
        self._page = page
        self._page.set_default_timeout(timeout)

    async def get_question(self):
        question_locator = self._page.locator(".belowBlackBox")
        await question_locator.wait_for(state="visible")
        return await question_locator.inner_text()

    async def get_context(self):
        log.info("Getting context")
        black_box = self._page.locator(".blackBox")
        log.info("Waiting for black box to be visible")
        await black_box.wait_for(state="visible")
        log.info("Getting context text")
        return await black_box.inner_text()

    async def get_content_type(self):
        context_type_locator = self._page.locator("#input-text-textarea")
        await context_type_locator.wait_for(state="visible")
        return await context_type_locator.get_attribute("placeholder") or ""

    async def get_image_description(self):
        final_image = self._page.locator(".finalRoundImage")
        await final_image.wait_for(state="visible")

        return await final_image.get_attribute("aria-label") or ""

    async def get_image_options(self):
        log.info("Getting image options")
        choices_container = self._page.locator("#choicesRegion > div > *")
        log.info("Waiting for choices container to be visible")
        await choices_container.first.wait_for(state="visible")
        log.info("Getting image options")

        options = await choices_container.all()
        log.info("Got image options")
        return [
            ImageChoiceOption(
                index=index,
                image_description=await option.locator("button").inner_text(),
            )
            for index, option in enumerate(options)
        ]

    async def get_text_voting_options(self):
        choices_container = self._page.locator("#choicesRegion > div > *")
        await choices_container.first.wait_for(state="visible")

        options = await choices_container.all()
        return [
            TextVotingOption(
                index=index,
                twist=await option.locator(".voteTwistHeader").inner_text()
                or await option.locator(".voteTwistFooter").inner_text(),
                player=await option.locator(".votePlayer").inner_text(),
                player_response=await option.locator(".voteResponse").inner_text(),
            )
            for index, option in enumerate(options)
        ]

    async def get_image_voting_options(self):
        choices_container = self._page.locator("#choicesRegion > div > *")
        await choices_container.first.wait_for(state="visible")

        options = await choices_container.all()
        return [
            ImageVotingOption(
                index=index,
                image_description=await option.locator(".voteThumbnail").get_attribute(
                    "aria-label"
                )
                or "",
                player=await option.locator(".votePlayer").inner_text(),
                twist=await option.locator(".voteTwistHeader").inner_text()
                or await option.locator(".voteTwistFooter").inner_text(),
            )
            for index, option in enumerate(options)
        ]

    async def submit_response(self, response: str):
        await self._page.fill("#input-text-textarea", response)
        await self._page.click("#buttons > div > div > button")

    async def select_option(self, index: int):
        choices_container = self._page.locator("#choicesRegion > div > *")
        await choices_container.first.wait_for(state="visible")

        options = await choices_container.all()
        await options[index].click()

    async def _get_options(self):
        choices_container = self._page.locator("#choicesRegion > div > *")
        await choices_container.first.wait_for(state="visible")

        return await choices_container.all()
