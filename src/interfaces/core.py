from typing import TypeVar

from src.interfaces.llm_proxy import BaseLLMProxy
from src.interfaces.repository import BaseRepository
from src.prompts import BasePromptGroup

Repository = TypeVar("Repository", bound=BaseRepository)
LLMProxy = TypeVar("LLMProxy", bound=BaseLLMProxy)
Prompts = TypeVar("Prompts", bound=BasePromptGroup)
