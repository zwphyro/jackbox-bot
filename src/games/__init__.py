from src.enums import GamesEnum
from src.prompts import get_prompts
from src.registry import GameRegistry

from survive_the_internet.bot import SurviveTheInternetBot
from survive_the_internet.llm_proxy import SurviveTheInternetLLMProxy
from survive_the_internet.repository import SurviveTheInternetRepository


def setup_registry():
    prompts = get_prompts()

    GameRegistry.register(
        GamesEnum.SurviveTheInternet,
        bot=SurviveTheInternetBot,
        repository=SurviveTheInternetRepository,
        llm_proxy=SurviveTheInternetLLMProxy,
        prompts=prompts.survive_the_internet,
    )
