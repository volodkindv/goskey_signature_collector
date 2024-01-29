from re import Match

from aiogram import F, Router  # noqa: WPS347
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from ..database.database import (
    change_appeal_file,
    change_appeal_text,
    change_appeal_visibility,
    create_appeal,
    get_appeal,
    get_appeal_signatures,
    get_appeals,
)
from ..filters.filters import IsAdminUser
from ..keyboards.appeal_kb import AdminCommandsLexicon, create_appeal_admin_keyboard
from ..lexicon.lexicon import Lexicon
from ..services.common import format_appeal_admin

router = Router()
router.message.filter(IsAdminUser())


class AppealForm(StatesGroup):
    change_name = State()
    change_file = State()


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
    await state.update_data(appeal_id=get_appeal_id_from_message(callback.message))
    await state.set_state(AppealForm.change_name)
    await callback.message.answer(text="Введите новый текст инициативы")
    await callback.answer()


@router.message(AppealForm.change_name)
async def admin_appeal_edit_name(message: Message, state: FSMContext) -> None:
    state_data = await state.get_data()
    await state.clear()

    appeal = await change_appeal_text(state_data["appeal_id"], message.text)

    response_text = format_appeal_admin(appeal)
    await message.answer(response_text, reply_markup=create_appeal_admin_keyboard(appeal.is_hidden))


@router.callback_query(F.data == AdminCommandsLexicon.publish)
async def admin_appeal_cb_publish(callback: CallbackQuery, state: FSMContext) -> None:
    appeal_id = get_appeal_id_from_message(callback.message)  # TODO
    appeal = await change_appeal_visibility(appeal_id, is_hidden=False)
    response_text = format_appeal_admin(appeal)
    await callback.message.answer(response_text, reply_markup=create_appeal_admin_keyboard(appeal.is_hidden))
    await callback.answer()


@router.callback_query(F.data == AdminCommandsLexicon.hide)
async def admin_appeal_cb_hide(callback: CallbackQuery, state: FSMContext) -> None:
    appeal_id = get_appeal_id_from_message(callback.message)  # TODO
    appeal = await change_appeal_visibility(appeal_id, is_hidden=True)
    response_text = format_appeal_admin(appeal)
    await callback.message.answer(response_text, reply_markup=create_appeal_admin_keyboard(appeal.is_hidden))
    await callback.answer()


@router.callback_query(F.data == AdminCommandsLexicon.get_signatures)
async def admin_appeal_get_signatures(callback: CallbackQuery) -> None:
    appeal_id = get_appeal_id_from_message(callback.message)  # TODO
    signatures = await get_appeal_signatures(appeal_id)
    for signature in signatures:
        await callback.message.answer_document(document=signature.file_id)
    await callback.answer()


@router.callback_query(F.data == AdminCommandsLexicon.view_file)
async def admin_appeal_cb_view_file(callback: CallbackQuery) -> None:
    appeal_id = get_appeal_id_from_message(callback.message)  # TODO
    appeal = await get_appeal(appeal_id)
    await callback.message.answer_document(appeal.file_id)
    await callback.answer()


def get_appeal_id_from_message(message: Message) -> int:
    return message.text.split()[0].replace("/admin_appeals_", "")


@router.callback_query(F.data == AdminCommandsLexicon.change_file)
async def admin_appeal_cb_edit_file(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(appeal_id=get_appeal_id_from_message(callback.message))
    await state.set_state(AppealForm.change_file)
    await callback.message.answer(text="Отправьте файл для подписания в формате PDF")
    await callback.answer()


@router.message(AppealForm.change_file, F.document)
async def admin_appeal_edit_file(message: Message, state: FSMContext) -> None:
    state_data = await state.get_data()
    await state.clear()
    appeal = await change_appeal_file(state_data["appeal_id"], message.document.file_id, message.document.file_name)
    response_text = format_appeal_admin(appeal)

    await message.answer(response_text, reply_markup=create_appeal_admin_keyboard(appeal.is_hidden))
