from functools import lru_cache

from pydantic import BaseModel
from pydantic_settings import BaseSettings


class BotConfig(BaseSettings):
    bot_token: str  # Токен для доступа к телеграм-боту
    database_uri: str


class Config(BaseModel):
    tg_bot: BotConfig


@lru_cache
def load_config() -> Config:
    return Config(
        tg_bot=BotConfig(),
    )
