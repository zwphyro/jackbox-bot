from functools import lru_cache
from typing import Any, Type
from pydantic import BaseModel, PrivateAttr
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    YamlConfigSettingsSource,
)

from src.settings import CONFIG_DIR


class BasePromptGroup(BaseModel):
    _base: str = PrivateAttr("")
    _style: str = PrivateAttr("")

    def _setup_context(self, base: str, style: str):
        self._base = base
        self._style = style

    def _format(self, field_name: str, **kwargs: Any) -> str:
        template = getattr(self, field_name)
        return template.format(base=self._base, style=self._style, **kwargs)


class SurviveTheInternetPrompts(BasePromptGroup):
    initial_response: str
    text_twist: str
    text_vote: str
    image_choice: str
    image_twist: str
    image_vote: str

    def get_initial_response(self):
        return self._format("initial_response")

    def get_text_twist(self, content_type: str):
        return self._format("text_twist", content_type=content_type)

    def get_text_vote(self):
        return self._format("text_vote")

    def get_image_choice(self):
        return self._format("image_choice")

    def get_image_twist(self):
        return self._format("image_twist")

    def get_image_vote(self):
        return self._format("image_vote")


class Prompts(BaseSettings):
    style: str
    base: str
    survive_the_internet: SurviveTheInternetPrompts

    def model_post_init(self, __context: Any) -> None:
        self.survive_the_internet._setup_context(base=self.base, style=self.style)

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ):
        return (
            init_settings,
            YamlConfigSettingsSource(
                settings_cls, yaml_file=CONFIG_DIR / "prompts.yaml"
            ),
            YamlConfigSettingsSource(
                settings_cls, yaml_file=CONFIG_DIR / "prompts.local.yaml"
            ),
            env_settings,
        )


@lru_cache
def get_prompts():
    return Prompts()  # type: ignore[no-call-issue]
