from aiogram import Bot, Dispatcher
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from .config_data.config import Config


class GlobalContext:
    bot: Bot
    dispatcher: Dispatcher
    config: Config
    engine: AsyncEngine
    async_session: async_sessionmaker

    @classmethod
    def get_session(cls) -> AsyncSession:
        return cls.async_session()
