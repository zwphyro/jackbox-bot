import json
from openai import AsyncOpenAI
from logging import getLogger

log = getLogger(__name__)


class LLMService:
    def __init__(self, client: AsyncOpenAI, model: str):
        self._client = client
        self._model = model

    async def _execute_prompt(self, system_prompt: str, json_payload: dict) -> str:
        payload_str = json.dumps(json_payload, ensure_ascii=False)
        log.debug(f"Sending payload to LLM: {payload_str}")

        response = await self._client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": payload_str},
            ],
        )
        result = response.choices[0].message.content.strip()
        log.debug(f"Received response from LLM: {result}")
        return result

    async def generate_initial_response(self, step_data: dict) -> str:
        log.info("Generating initial response without context.")
        system_prompt = "You are playing 'Survive the Internet'. Provide a short, naive, but funny answer to the question in the JSON payload. Max 10 words."
        return await self._execute_prompt(system_prompt, step_data)

    async def generate_twist_response(self, step_data: dict) -> str:
        log.info("Generating twist response with context.")
        system_prompt = "You are playing 'Survive the Internet'. You will receive a JSON with 'context_text' and 'prompt_text'. Write a short, cynical, or hilariously out-of-context caption that makes the 'context_text' look terrible or absurd. Max 10 words."
        return await self._execute_prompt(system_prompt, step_data)

    async def choose_text_vote(self, step_data: dict) -> int:
        log.info("Selecting text vote.")
        system_prompt = "You will receive a JSON with voting options. Return ONLY the integer 'index' of the funniest and most brutal response. Do not output any other text."
        result = await self._execute_prompt(system_prompt, step_data)
        try:
            return int(result)
        except ValueError:
            log.warning(f"Failed to parse integer from LLM: {result}. Defaulting to 0.")
            return 0

    async def choose_image_response(self, step_data: dict) -> int:
        log.info("Selecting option for image phase.")
        system_prompt = "You will receive a JSON with a question and multiple choice options. Return ONLY the integer 'index' of the option that has the most comedic potential. Do not output any other text."
        result = await self._execute_prompt(system_prompt, step_data)
        try:
            return int(result)
        except ValueError:
            log.warning(f"Failed to parse integer from LLM: {result}. Defaulting to 0.")
            return 0

    async def generate_image_twist(self, step_data: dict) -> str:
        log.info("Generating image twist comment.")
        system_prompt = "You will receive a JSON with 'image_description' and 'prompt_text'. Write a funny, short caption based on the prompt that makes the image description hilarious. Max 10 words."
        return await self._execute_prompt(system_prompt, step_data)

    async def choose_image_vote(self, step_data: dict) -> int:
        log.info("Selecting image vote.")
        system_prompt = "You will receive a JSON with image voting options containing descriptions and responses. Return ONLY the integer 'index' of the funniest combination. Do not output any other text."
        result = await self._execute_prompt(system_prompt, step_data)
        try:
            return int(result)
        except ValueError:
            log.warning(f"Failed to parse integer from LLM: {result}. Defaulting to 0.")
            return 0
