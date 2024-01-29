from aiogram import F, Router  # noqa: WPS347
from aiogram.filters import Command
from aiogram.types import Message

from ..database.database import create_appeal, get_appeals
from ..filters.filters import IsAdminUser
from ..keyboards.appeal_kb import create_appeal_admin_keyboard
from ..lexicon.lexicon import Lexicon
from ..services.common import format_appeal_admin

router = Router()
router.message.filter(IsAdminUser())


@router.message(
    Command(commands="admin"),
)
async def admin_menu(message: Message) -> None:
    await message.answer(Lexicon.admin_menu)


@router.message(F.text.startswith("/admin_appeals"))
async def admin_appeals_list(message: Message) -> None:
    appeals = await get_appeals(show_hidden=True)
    lines = ["Список инициатив (админка)"]
    lines.extend([format_appeal_admin(appeal) for appeal in appeals])
    await message.answer("\n".join(lines))


@router.message(F.text.startswith("/admin_add_appeal"))
async def admin_appeals_add(message: Message) -> None:
    # можно сразу создать инициативу, но не публиковать ее.
    new_appeal = await create_appeal()
    await message.answer(format_appeal_admin(new_appeal), reply_markup=create_appeal_admin_keyboard())
