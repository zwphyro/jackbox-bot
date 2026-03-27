from functools import lru_cache
from math import ceil
from pathlib import Path
from typing import Annotated, Type
from pydantic import BaseModel, StringConstraints
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    YamlConfigSettingsSource,
)


class PlaywrightSettings(BaseModel):
    user_agent: str
    timeout_min: float

    @property
    def timeout_ms(self):
        return ceil(self.timeout_min * 60 * 1000)


class JackboxSettings(BaseModel):
    join_url: str
    bot_name: str


class LLMSettings(BaseModel):
    api_key: Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)]
    base_url: str | None = None
    model: str


class LoggingSettings(BaseModel):
    level: str


BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"


class Settings(BaseSettings):
    jackbox: JackboxSettings
    llm: LLMSettings
    playwright: PlaywrightSettings
    logging: LoggingSettings

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
                settings_cls,
                yaml_file=[
                    CONFIG_DIR / "settings.yaml",
                    CONFIG_DIR / "settings.local.yaml",
                ],
            ),
            env_settings,
        )


@lru_cache
def get_settings():
    return Settings()  # type: ignore[no-call-issue]
