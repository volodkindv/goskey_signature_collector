from __future__ import annotations

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class CommandsLexicon:
    sign = "Подписать"
    show_manual = "Инструкция"


def create_appeal_keyboard() -> InlineKeyboardMarkup:
    button_sign = InlineKeyboardButton(text="Подписать", callback_data=CommandsLexicon.sign)
    button_show_manual = InlineKeyboardButton(text="Инструкция", callback_data=CommandsLexicon.show_manual)

    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(button_sign, button_show_manual)
    return kb_builder.as_markup()
