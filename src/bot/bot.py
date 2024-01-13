import logging
from functools import lru_cache

from aiogram import Bot, Dispatcher

from .config_data.config import load_config
from .handlers import common_handlers, user_handlers
from .keyboards.main_menu import set_main_menu

logger = logging.getLogger(__name__)


@lru_cache
def get_dispatcher() -> Dispatcher:
    dp = Dispatcher()
    all_routers = [
        common_handlers.router,
        user_handlers.router,
    ]
    for router in all_routers:
        dp.include_router(router)
    return dp


@lru_cache
def get_bot(bot_token: str) -> Bot:
    return Bot(token=bot_token, parse_mode="HTML")


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )

    logger.info("Starting bot")

    config = load_config()
    bot = get_bot(config.tg_bot.bot_token)
    dispatcher = get_dispatcher()

    await set_main_menu(bot)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)
