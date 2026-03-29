from src.enums import GamesEnum
from src.interfaces.bot import BaseBot
from src.interfaces.llm_proxy import BaseLLMProxy
from src.interfaces.repository import BaseRepository
from src.prompts import BasePromptGroup
from src.schemas import GameEntry


class GameRegistry:
    _games: dict[GamesEnum, GameEntry] = {}

    @classmethod
    def register(
        cls,
        game: GamesEnum,
        bot: type[BaseBot],
        repository: type[BaseRepository],
        llm_proxy: type[BaseLLMProxy],
        prompts: BasePromptGroup,
    ):
        cls._games[game] = GameEntry(
            bot=bot, repository=repository, llm_proxy=llm_proxy, prompts=prompts
        )

    @classmethod
    def get_game_entry(cls, game: GamesEnum):
        return cls._games.get(game)
