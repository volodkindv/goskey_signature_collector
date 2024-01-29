from functools import lru_cache

from aiogram import Router
from aiogram.filters import Filter
from aiogram.types import Message

from ..config_data.config import load_config

router = Router()


@lru_cache
def admin_user_ids() -> list[str]:
    return load_config().tg_bot.admin_user_ids.split(",")


class IsAdminUser(Filter):
    async def __call__(self, message: Message) -> bool:
        return str(message.from_user.id) in admin_user_ids()
