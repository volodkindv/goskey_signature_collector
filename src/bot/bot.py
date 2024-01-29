import logging

from aiogram import Bot, Dispatcher, Router
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from .config_data.config import Config, load_config
from .context import GlobalContext
from .database.database import init_models
from .handlers import admin_handlers, common_handlers, user_handlers
from .keyboards.main_menu import set_main_menu

logger = logging.getLogger(__name__)


def get_routers() -> list[Router]:
    return [
        common_handlers.router,
        user_handlers.router,
        admin_handlers.router,
    ]


def get_dispatcher() -> Dispatcher:
    return GlobalContext.dispatcher


def get_bot() -> Bot:
    return GlobalContext.bot


async def init_app(config: Config) -> None:
    GlobalContext.config = config
    GlobalContext.bot = Bot(token=config.tg_bot.bot_token, parse_mode="HTML")

    dp = Dispatcher()
    for router in get_routers():
        dp.include_router(router)

    GlobalContext.dispatcher = dp

    GlobalContext.engine = create_async_engine(GlobalContext.config.tg_bot.database_uri, echo=True)
    GlobalContext.async_session = async_sessionmaker(GlobalContext.engine, class_=AsyncSession, expire_on_commit=False)

    await init_models()


async def main() -> None:
    await init_app(load_config())

    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )

    logger.info("Starting bot")

    await set_main_menu(GlobalContext.bot)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await GlobalContext.bot.delete_webhook(drop_pending_updates=True)
    await GlobalContext.dispatcher.start_polling(GlobalContext.bot)
