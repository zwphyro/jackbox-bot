from abc import ABC
from logging import getLogger
from typing import Generic, TypeVar

from openai import AsyncOpenAI

from src.schemas import BasePromptPayload
from src.prompts import BasePromptGroup

log = getLogger()

Prompts = TypeVar("Prompts", bound=BasePromptGroup)


class BaseLLMProxy(ABC, Generic[Prompts]):
    def __init__(self, client: AsyncOpenAI, model: str, prompts: Prompts):
        self._client = client
        self._model = model
        self._prompts = prompts

    async def _execute_prompt(
        self, system_prompt: str, request: BasePromptPayload, temperature: float
    ):
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
