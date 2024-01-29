from functools import lru_cache

from aiogram import Router
from aiogram.filters import Filter
from aiogram.types import Message

from ..context import GlobalContext

router = Router()


@lru_cache
def admin_user_ids() -> list[str]:
    return GlobalContext.config.tg_bot.admin_user_ids.split(",")


class IsAdminUser(Filter):
    async def __call__(self, message: Message) -> bool:
        return str(message.from_user.id) in admin_user_ids()
