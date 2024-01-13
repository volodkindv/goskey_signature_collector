import logging

from aiogram import Bot, Dispatcher

from .config_data.config import load_config
from .handlers import common_handlers
from .keyboards.main_menu import set_main_menu

logger = logging.getLogger(__name__)


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )

    logger.info("Starting bot")

    config = load_config()

    bot = Bot(token=config.tg_bot.bot_token, parse_mode="HTML")
    dp = Dispatcher()

    await set_main_menu(bot)

    all_routers = [
        common_handlers.router,
    ]
    for router in all_routers:
        dp.include_router(router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
