from __future__ import annotations
from abc import ABC, abstractmethod
import asyncio
from logging import getLogger
from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from src.interfaces.llm_proxy import BaseLLMProxy
    from src.interfaces.repository import BaseRepository

Repository = TypeVar("Repository", bound=BaseRepository)
LLMProxy = TypeVar("LLMProxy", bound=BaseLLMProxy)

log = getLogger(__name__)


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

    async def run(self):
        for task_coroutine in self.tasks:
            await self._execute_step(task_coroutine)

    async def _execute_step(self, coroutine: callable, max_retries: int = 3):
        phase_name = coroutine.__name__
        for i in range(max_retries):
            attempt = i + 1
            try:
                log.info(
                    f"Attempting queue task: {phase_name} (Attempt {attempt}/{max_retries})"
                )
                await coroutine()
                log.info(f"Task {phase_name} executed successfully.")
                return
            except Exception as e:
                log.error(f"Task {phase_name} failed on attempt {attempt}: {e}")
                if attempt == max_retries:
                    log.critical(
                        f"Task {phase_name} exhausted all retries. Proceeding to next queue item."
                    )
                await asyncio.sleep(2)
