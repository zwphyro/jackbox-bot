from openai import AsyncOpenAI
from playwright.async_api import Page

from src.enums import GamesEnum
from src.registry import GameRegistry


class GameFactory:
    def __init__(
        self,
        page: Page,
        client: AsyncOpenAI,
        timeout: int,
        model: str,
    ):
        self._page = page
        self._client = client
        self._timeout = timeout
        self._model = model

    def create_bot(self, game_type: GamesEnum):
        game_entry = GameRegistry.get_game_entry(game_type)
        if game_entry is None:
            raise ValueError(f"Game type '{game_type}' is not registered")

        repository = game_entry.create_repository(self._page, self._timeout)
        llm_proxy = game_entry.create_llm_proxy(self._client, self._model)
        bot = game_entry.create_bot(repository, llm_proxy)

        return bot
