from aiogram import F, Router  # noqa: WPS347
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from ..database.database import get_current_appeals
from ..keyboards.appeal_kb import CommandsLexicon, create_appeal_keyboard
from ..schemas.schemas import Appeal

router = Router()


def format_appeal(appeal: Appeal) -> str:
    return f"/appeals_{appeal.id} {appeal.name}"


@router.message(Command(commands="appeals"))
async def process_appeals_list_command(message: Message) -> None:
    appeals = await get_current_appeals()
    lines = ["Список инициатив"]
    lines.extend([format_appeal(appeal) for appeal in appeals])
    await message.answer("\n".join(lines))


@router.message(F.text.startswith("/appeals_"))
async def process_appeals_item_command(message: Message) -> None:
    await message.answer("Инициатива 1", reply_markup=create_appeal_keyboard())


@router.callback_query(F.data == CommandsLexicon.sign)
async def process_appeal_send_cb(callback: CallbackQuery) -> None:
    document = "https://github.com/volodkindv/goskey_signature_collector/files/13978167/Appeal_1_sample.pdf"
    # TODO научиться отправлять по id.

    await callback.message.answer(
        text="Ознакомьтесь с документом ниже. Подпишите его Госключом и отправьте в этот чат файл подписи.",
    )
    await callback.message.answer_document(document=document)
    await callback.answer()


@router.callback_query(F.data == CommandsLexicon.show_manual)
async def process_appeal_manual_cb(callback: CallbackQuery) -> None:
    text = (
        "Инструкция для подписания документа: "
        + "https://github.com/volodkindv/goskey_signature_collector/wiki/%D0%9F%D0%BE%D0%B4%D0%BF%D0%B8%D1%81%D0%B0%D0%BD%D0%B8%D0%B5-%D0%B4%D0%BE%D0%BA%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D0%B0-%D1%87%D0%B5%D1%80%D0%B5%D0%B7-%D0%93%D0%BE%D1%81%D0%BA%D0%BB%D1%8E%D1%87"
    )
    await callback.message.answer(text=text, reply_markup=ReplyKeyboardRemove())


@router.message(F.document)
async def process_file_received(message: Message) -> None:
    # TODO понимать, к какому обращению ее приобщить.
    # добавить проверку, что это именно подпись.
    # и хорошо бы сразу валидацию.
    await message.answer(text="Спасибо, ваша подпись будет приложена к обращению", reply_markup=ReplyKeyboardRemove())
