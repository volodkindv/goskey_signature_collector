from aiogram import F, Router  # noqa: WPS347
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from ..database.database import get_current_appeals
from ..filters.filters import IsAdminUser
from ..keyboards.appeal_kb import CommandsLexicon, create_appeal_keyboard
from ..schemas.schemas import Appeal

router = Router()
router.message.filter(IsAdminUser())


# Действия с обращениями: список, одно, изменение, удаление.
# Список и одно уже есть. Не хватает, может, кнопок на редактирование.
# Удалять насовсем не будем. Только пометку на удаление ставить.


def format_appeal(appeal: Appeal) -> str:
    return f"/appeals_{appeal.id} {appeal.name}"


@router.message(
    Command(commands="ping_admin"),
)
async def ping_admin(message: Message) -> None:
    await message.answer("ping")
