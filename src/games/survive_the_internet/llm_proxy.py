from logging import getLogger

from src.interfaces.llm_proxy import BaseLLMProxy
from src.prompts import SurviveTheInternetPrompts
from src.games.survive_the_internet.schemas import (
    ImageChoiceRequest,
    ImageTwistRequest,
    ImageVoteRequest,
    InitialRequest,
    TextVoteRequest,
    TwistRequest,
)

log = getLogger(__name__)


class SurviveTheInternetLLMProxy(BaseLLMProxy[SurviveTheInternetPrompts]):
    async def generate_initial_response(self, request: InitialRequest):
        log.info("Generating initial response without context.")
        return await self._execute_prompt(
            self._prompts.get_initial_response(), request, temperature=0.7
        )

    async def generate_text_twist(self, request: TwistRequest):
        log.info("Generating twist response with context.")
        return await self._execute_prompt(
            self._prompts.get_text_twist(request.content_type), request, temperature=0.9
        )

    async def choose_text_vote(self, request: TextVoteRequest):
        log.info("Selecting text vote.")
        result = await self._execute_prompt(
            self._prompts.get_text_vote(), request, temperature=0
        )
        try:
            return int(result)
        except ValueError:
            log.warning(f"Failed to parse integer from LLM: {result}. Defaulting to 0.")
            return 0

    async def choose_image(self, request: ImageChoiceRequest):
        log.info("Selecting option for image phase.")
        result = await self._execute_prompt(
            self._prompts.get_image_choice(), request, temperature=0
        )
        try:
            return int(result)
        except ValueError:
            log.warning(f"Failed to parse integer from LLM: {result}. Defaulting to 0.")
            return 0

    async def generate_image_twist(self, request: ImageTwistRequest):
        log.info("Generating image twist comment.")
        return await self._execute_prompt(
            self._prompts.get_image_twist(), request, temperature=0.9
        )

    async def choose_image_vote(self, request: ImageVoteRequest):
        log.info("Selecting image vote.")
        result = await self._execute_prompt(
            self._prompts.get_image_vote(), request, temperature=0
        )
        try:
            return int(result)
        except ValueError:
            log.warning(f"Failed to parse integer from LLM: {result}. Defaulting to 0.")
            return 0
