from __future__ import annotations
from abc import abstractmethod

from pydantic import BaseModel

from src.interfaces.core import (
    BotProtocol,
    LLMProxyProtocol,
    RepositoryProtocol,
    PromptGroupProtocol,
)


class BasePromptPayload(BaseModel):
    @abstractmethod
    def model_dump_prompt(self):
        raise NotImplementedError


class GameEntry(BaseModel):
    bot: "type[BotProtocol]"
    repository: "type[RepositoryProtocol]"
    llm_proxy: "type[LLMProxyProtocol]"
    prompts: "PromptGroupProtocol"

    model_config = {"arbitrary_types_allowed": True}


GameEntry.model_rebuild()
