import os
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    join_url: str = Field(..., alias="JOIN_URL")
    bot_name: str = Field(..., alias="BOT_NAME")

    llm_api_key: str = Field(..., alias="LLM_API_KEY", min_length=1)
    llm_base_url: str | None = Field(None, alias="LLM_BASE_URL")
    llm_model: str = Field(..., alias="LLM_MODEL")

    log_level: str = Field("INFO", alias="LOG_LEVEL")

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", ".env"),
        extra="ignore",
    )


_settings = None


def get_settings():
    global _settings

    if _settings is None:
        _settings = Settings()  # type: ignore[no-call-issue]

    return _settings
