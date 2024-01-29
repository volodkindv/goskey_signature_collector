from re import Match

from aiogram import F, Router  # noqa: WPS347
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from ..database.database import change_appeal_visibility, create_appeal, edit_appeal, get_appeal, get_appeals
from ..filters.filters import IsAdminUser
from ..keyboards.appeal_kb import AdminCommandsLexicon, create_appeal_admin_keyboard
from ..lexicon.lexicon import Lexicon
from ..services.common import format_appeal_admin

router = Router()
router.message.filter(IsAdminUser())


class AppealForm(StatesGroup):
    name = State()


@router.message(Command(commands="admin"))
async def admin_menu(message: Message) -> None:
    await message.answer(Lexicon.admin_menu)


@router.message(F.text.startswith("/admin_appeals_list"))
async def admin_appeals_list(message: Message) -> None:
    appeals = await get_appeals(show_hidden=True)
    lines = ["Список инициатив (админка)"]
    lines.extend([format_appeal_admin(appeal) for appeal in appeals])
    await message.answer("\n".join(lines))


@router.message(F.text.startswith("/admin_appeals_add"))
async def admin_appeals_add(message: Message) -> None:
    # можно сразу создать инициативу, но не публиковать ее.
    new_appeal = await create_appeal()
    await message.answer(format_appeal_admin(new_appeal), reply_markup=create_appeal_admin_keyboard(True))


@router.message(F.text.regexp(r"^/admin_appeals_(\d+)").as_("match"))
async def admin_appeals_item(message: Message, match: Match) -> None:
    digits = match.group(1)
    appeal = await get_appeal(str(digits))
    if appeal is None:
        await message.answer("Инициатива не найдена")
        return

    await message.answer(format_appeal_admin(appeal), reply_markup=create_appeal_admin_keyboard(appeal.is_hidden))


@router.callback_query(F.data == AdminCommandsLexicon.name)
async def admin_appeal_cb_edit_name(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(appeal_id=1)
    await state.set_state(AppealForm.name)
    await callback.message.answer(text="Введите новый текст инициативы")
    await callback.answer()


@router.message(AppealForm.name)
async def admin_appeal_edit_name(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    await state.clear()

    appeal = await edit_appeal(data["appeal_id"], message.text)

    response_text = format_appeal_admin(appeal)
    await message.answer(response_text, reply_markup=create_appeal_admin_keyboard(appeal.is_hidden))


@router.callback_query(F.data == AdminCommandsLexicon.publish)
async def admin_appeal_cb_publish(callback: CallbackQuery, state: FSMContext) -> None:
    appeal_id = callback.message.text.split()[0].replace("/admin_appeals_", "")  # TODO
    appeal = await change_appeal_visibility(appeal_id, is_hidden=False)
    response_text = format_appeal_admin(appeal)
    await callback.message.answer(response_text, reply_markup=create_appeal_admin_keyboard(appeal.is_hidden))
    await callback.answer()


@router.callback_query(F.data == AdminCommandsLexicon.hide)
async def admin_appeal_cb_publish(callback: CallbackQuery, state: FSMContext) -> None:
    appeal_id = callback.message.text.split()[0].replace("/admin_appeals_", "")  # TODO
    appeal = await change_appeal_visibility(appeal_id, is_hidden=True)
    response_text = format_appeal_admin(appeal)
    await callback.message.answer(response_text, reply_markup=create_appeal_admin_keyboard(appeal.is_hidden))
    await callback.answer()
