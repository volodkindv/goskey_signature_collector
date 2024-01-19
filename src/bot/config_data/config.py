
from pydantic import BaseModel
from pydantic_settings import BaseSettings


class BotConfig(BaseSettings):
    bot_token: str            # Токен для доступа к телеграм-боту


class Config(BaseModel):
    tg_bot: BotConfig


def load_config() -> Config:
    return Config(
        tg_bot=BotConfig(),
    )
