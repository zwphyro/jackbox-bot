from __future__ import annotations
from typing import TYPE_CHECKING

from src.enums import GamesEnum
from src.schemas import GameEntry

if TYPE_CHECKING:
    from src.interfaces.core import (
        BotProtocol,
        LLMProxyProtocol,
        RepositoryProtocol,
        PromptGroupProtocol,
    )


class GameRegistry:
    _games: dict[GamesEnum, GameEntry] = {}

    @classmethod
    def register(
        cls,
        game: GamesEnum,
        bot: type[BotProtocol],
        repository: type[RepositoryProtocol],
        llm_proxy: type[LLMProxyProtocol],
        prompts: PromptGroupProtocol,
    ):
        cls._games[game] = GameEntry(
            bot=bot, repository=repository, llm_proxy=llm_proxy, prompts=prompts
        )

    @classmethod
    def get_game_entry(cls, game: GamesEnum):
        return cls._games.get(game)
