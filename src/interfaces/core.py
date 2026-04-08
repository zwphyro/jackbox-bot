from __future__ import annotations
from abc import abstractmethod
from typing import Protocol, runtime_checkable, TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from src.schemas import BasePromptPayload


@runtime_checkable
class BotProtocol(Protocol):
    """Protocol for bot interface"""

    @abstractmethod
    def tasks(self):
        raise NotImplementedError

    @abstractmethod
    async def run(self):
        raise NotImplementedError


@runtime_checkable
class LLMProxyProtocol(Protocol):
    """Protocol for LLM proxy interface"""

    @abstractmethod
    async def _execute_prompt(
        self, system_prompt: str, request: "BasePromptPayload", temperature: float
    ):
        raise NotImplementedError


@runtime_checkable
class RepositoryProtocol(Protocol):
    """Protocol for repository interface"""

    pass


@runtime_checkable
class PromptGroupProtocol(Protocol):
    """Protocol for prompt group interface"""

    pass


Repository = TypeVar("Repository", bound=RepositoryProtocol)
LLMProxy = TypeVar("LLMProxy", bound=LLMProxyProtocol)
Prompts = TypeVar("Prompts", bound=PromptGroupProtocol)
