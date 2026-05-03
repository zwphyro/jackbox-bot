from abc import abstractmethod

from openai import AsyncOpenAI
from playwright.async_api import Page
from pydantic import BaseModel

from src.interfaces.bot import BaseBot
from src.interfaces.llm_proxy import BaseLLMProxy
from src.interfaces.repository import BaseRepository
from src.prompts import BasePromptGroup


class BasePromptPayload(BaseModel):
    @abstractmethod
    def model_dump_prompt(self):
        raise NotImplementedError


class GameEntry(BaseModel):
    bot: type[BaseBot]
    repository: type[BaseRepository]
    llm_proxy: type[BaseLLMProxy]
    prompts: BasePromptGroup

    model_config = {"arbitrary_types_allowed": True}

    def create_repository(self, page: Page, timeout: int):
        return self.repository(page, timeout)

    def create_llm_proxy(self, client: AsyncOpenAI, model: str):
        return self.llm_proxy(client, model, self.prompts)

    def create_bot(
        self,
        repository: BaseRepository,
        llm_proxy: BaseLLMProxy,
    ):
        return self.bot(repository, llm_proxy)


GameEntry.model_rebuild()
