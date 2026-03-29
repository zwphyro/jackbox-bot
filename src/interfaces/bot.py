from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from src.interfaces.llm_proxy import BaseLLMProxy
from src.interfaces.repository import BaseRepository

Repository = TypeVar("Repository", bound=BaseRepository)
LLMProxy = TypeVar("LLMProxy", bound=BaseLLMProxy)


class BaseBot(ABC, Generic[Repository, LLMProxy]):
    def __init__(
        self,
        repository: Repository,
        llm_proxy: LLMProxy,
    ):
        self._repository = repository
        self._llm_proxy = llm_proxy

    @property
    @abstractmethod
    def tasks(self):
        raise NotImplementedError
