from openai import AsyncOpenAI
from logging import getLogger

from src.prompts import SurviveTheInternetPrompts
from src.games.survive_the_internet.schemas import (
    BasePromptPayload,
    ImageChoiceRequest,
    ImageTwistRequest,
    ImageVoteRequest,
    InitialRequest,
    TextVoteRequest,
    TwistRequest,
)

log = getLogger(__name__)


class SurviveTheInternetLLMProxy:
    def __init__(
        self, client: AsyncOpenAI, model: str, prompts: SurviveTheInternetPrompts
    ):
        self._client = client
        self._model = model
        self._prompts = prompts

    async def _execute_prompt(
        self, system_prompt: str, request: BasePromptPayload, temperature: float
    ) -> str:
        content = request.model_dump_prompt()
        log.debug(f"Sending payload to LLM: {content}")

        response = await self._client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": content},
            ],
            temperature=temperature,
        )
        result = response.choices[0].message.content.strip()
        log.debug(f"Received response from LLM: {result}")
        return result

    async def generate_initial_response(self, request: InitialRequest) -> str:
        log.info("Generating initial response without context.")
        return await self._execute_prompt(
            self._prompts.get_initial_response(), request, temperature=0.7
        )

    async def generate_text_twist(self, request: TwistRequest) -> str:
        log.info("Generating twist response with context.")
        return await self._execute_prompt(
            self._prompts.get_text_twist(request.content_type), request, temperature=0.9
        )

    async def choose_text_vote(self, request: TextVoteRequest) -> int:
        log.info("Selecting text vote.")
        result = await self._execute_prompt(
            self._prompts.get_text_vote(), request, temperature=0
        )
        try:
            return int(result)
        except ValueError:
            log.warning(f"Failed to parse integer from LLM: {result}. Defaulting to 0.")
            return 0

    async def choose_image(self, request: ImageChoiceRequest) -> int:
        log.info("Selecting option for image phase.")
        result = await self._execute_prompt(
            self._prompts.get_image_choice(), request, temperature=0
        )
        try:
            return int(result)
        except ValueError:
            log.warning(f"Failed to parse integer from LLM: {result}. Defaulting to 0.")
            return 0

    async def generate_image_twist(self, request: ImageTwistRequest) -> str:
        log.info("Generating image twist comment.")
        return await self._execute_prompt(
            self._prompts.get_image_twist(), request, temperature=0.9
        )

    async def choose_image_vote(self, request: ImageVoteRequest) -> int:
        log.info("Selecting image vote.")
        result = await self._execute_prompt(
            self._prompts.get_image_vote(), request, temperature=0
        )
        try:
            return int(result)
        except ValueError:
            log.warning(f"Failed to parse integer from LLM: {result}. Defaulting to 0.")
            return 0
