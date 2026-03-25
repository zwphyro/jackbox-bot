from openai import AsyncOpenAI
from logging import getLogger

from src.prompts import (
    BASE_PROMPT,
    CHOOSE_IMAGE_PROMPT,
    IMAGE_TWIST_PROMPT,
    IMAGE_VOTE_PROMPT,
    INITIAL_RESPONSE_PROMPT,
    TEXT_TWIST_PROMPT,
    TEXT_VOTE_PROMPT,
)
from src.schemas import (
    ImageChoiceRequest,
    ImageTwistRequest,
    ImageVoteRequest,
    InitialRequest,
    TextVoteRequest,
    TwistRequest,
)

log = getLogger(__name__)


class LLMService:
    def __init__(self, client: AsyncOpenAI, model: str):
        self._client = client
        self._model = model

    async def _execute_prompt(
        self, system_prompt: str, request: str, temperature: float
    ) -> str:
        log.debug(f"Sending payload to LLM: {request}")

        response = await self._client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system", "content": BASE_PROMPT + "\n" + system_prompt},
                {"role": "user", "content": request},
            ],
            temperature=temperature,
        )
        result = response.choices[0].message.content.strip()
        log.debug(f"Received response from LLM: {result}")
        return result

    async def generate_initial_response(self, request: InitialRequest) -> str:
        log.info("Generating initial response without context.")
        return await self._execute_prompt(
            INITIAL_RESPONSE_PROMPT, request.model_dump_json(), temperature=0.7
        )

    async def generate_text_twist(self, request: TwistRequest) -> str:
        log.info("Generating twist response with context.")
        return await self._execute_prompt(
            TEXT_TWIST_PROMPT, request.model_dump_json(), temperature=0.9
        )

    async def choose_text_vote(self, request: TextVoteRequest) -> int:
        log.info("Selecting text vote.")
        result = await self._execute_prompt(
            TEXT_VOTE_PROMPT, request.model_dump_json(), temperature=0
        )
        try:
            return int(result)
        except ValueError:
            log.warning(f"Failed to parse integer from LLM: {result}. Defaulting to 0.")
            return 0

    async def choose_image(self, request: ImageChoiceRequest) -> int:
        log.info("Selecting option for image phase.")
        result = await self._execute_prompt(
            CHOOSE_IMAGE_PROMPT, request.model_dump_json(), temperature=0
        )
        try:
            return int(result)
        except ValueError:
            log.warning(f"Failed to parse integer from LLM: {result}. Defaulting to 0.")
            return 0

    async def generate_image_twist(self, request: ImageTwistRequest) -> str:
        log.info("Generating image twist comment.")
        return await self._execute_prompt(
            IMAGE_TWIST_PROMPT, request.model_dump_json(), temperature=0.9
        )

    async def choose_image_vote(self, request: ImageVoteRequest) -> int:
        log.info("Selecting image vote.")
        result = await self._execute_prompt(
            IMAGE_VOTE_PROMPT, request.model_dump_json(), temperature=0
        )
        try:
            return int(result)
        except ValueError:
            log.warning(f"Failed to parse integer from LLM: {result}. Defaulting to 0.")
            return 0
