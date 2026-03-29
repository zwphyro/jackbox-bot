from abc import abstractmethod

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
