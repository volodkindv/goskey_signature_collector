from re import Match

from aiogram import F, Router  # noqa: WPS347
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from ..database.database import get_appeal, get_appeals, get_or_create_user, post_user_signature
from ..keyboards.appeal_kb import CommandsLexicon, create_appeal_keyboard
from ..services.common import format_appeal

router = Router()


class AppealForm(StatesGroup):
    add_file = State()


def get_appeal_id_from_message(message: Message) -> int:
    return message.text.split()[0].replace("/appeals_", "")


@router.message(Command(commands="appeals"))
async def process_appeals_list_command(message: Message) -> None:
    appeals = await get_appeals()
    lines = ["Список инициатив"]
    lines.extend([format_appeal(appeal) for appeal in appeals])
    await message.answer("\n".join(lines))


@router.message(F.text.regexp(r"^/appeals_(\d+)").as_("match"))
async def process_appeals_item_command(message: Message, match: Match) -> None:
    digits = match.group(1)
    appeal = await get_appeal(str(digits))
    if appeal is None:
        await message.answer("Инициатива не найдена")
        return

    await message.answer(format_appeal(appeal), reply_markup=create_appeal_keyboard())


@router.callback_query(F.data == CommandsLexicon.show_manual)
async def process_appeal_manual_cb(callback: CallbackQuery) -> None:
    text = (
        "Инструкция для подписания документа: "
        + "https://github.com/volodkindv/goskey_signature_collector/wiki/%D0%9F%D0%BE%D0%B4%D0%BF%D0%B8%D1%81%D0%B0%D0%BD%D0%B8%D0%B5-%D0%B4%D0%BE%D0%BA%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D0%B0-%D1%87%D0%B5%D1%80%D0%B5%D0%B7-%D0%93%D0%BE%D1%81%D0%BA%D0%BB%D1%8E%D1%87"
    )
    await callback.message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await callback.answer()


@router.callback_query(F.data == CommandsLexicon.sign)
async def process_appeal_send_cb(callback: CallbackQuery, state: FSMContext) -> None:
    appeal_id = get_appeal_id_from_message(callback.message)
    appeal = await get_appeal(appeal_id)
    await state.update_data(appeal_id=appeal_id)
    await state.set_state(AppealForm.add_file)

    await callback.message.answer(
        text="Ознакомьтесь с документом ниже. Подпишите его Госключом и отправьте в этот чат файл подписи.",
    )
    await callback.message.answer_document(document=appeal.file_id)
    # TODO добавить возможность отказа
    await callback.answer()


@router.message(AppealForm.add_file, F.document)
async def process_file_received(message: Message, state: FSMContext) -> None:
    state_data = await state.get_data()
    await state.clear()
    user = await get_or_create_user(message.from_user.id, message.from_user.full_name)
    appeal = await get_appeal(state_data["appeal_id"])
    await post_user_signature(user, appeal, message.document.file_id, message.document.file_name)
    await message.answer(text="Спасибо, ваша подпись будет приложена к обращению", reply_markup=ReplyKeyboardRemove())
