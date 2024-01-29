from __future__ import annotations

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class CommandsLexicon:
    sign = "Подписать"
    show_manual = "Инструкция"


class AdminCommandsLexicon:
    name = "Сменить название"
    publish = "Опубликовать"
    hide = "Снять с публикации"
    change_file = "Заменить файл для подписания"
    view_file = "Посмотреть файл"
    get_signatures = "Получить файлы подписей"


def create_appeal_keyboard() -> InlineKeyboardMarkup:
    button_sign = InlineKeyboardButton(text="Подписать", callback_data=CommandsLexicon.sign)
    button_show_manual = InlineKeyboardButton(text="Инструкция", callback_data=CommandsLexicon.show_manual)

    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(button_sign, button_show_manual)
    return kb_builder.as_markup()


def create_appeal_admin_keyboard(is_hidden: bool) -> InlineKeyboardMarkup:
    button_change_name = InlineKeyboardButton(text="Сменить название", callback_data=AdminCommandsLexicon.name)
    if is_hidden:
        button_change_state = InlineKeyboardButton(text="Опубликовать", callback_data=AdminCommandsLexicon.publish)
    else:
        button_change_state = InlineKeyboardButton(text="Снять с публикации", callback_data=AdminCommandsLexicon.hide)

    button_change_file = InlineKeyboardButton(
        text="Заменить файл для подписания",
        callback_data=AdminCommandsLexicon.change_file,
    )
    button_view_file = InlineKeyboardButton(text="Посмотреть файл", callback_data=AdminCommandsLexicon.view_file)
    button_get_signatures = InlineKeyboardButton(
        text="Получить файлы подписей",
        callback_data=AdminCommandsLexicon.get_signatures,
    )

    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        button_change_name,
        button_change_state,
    )
    kb_builder.row(
        button_change_file,
        button_view_file,
    )
    kb_builder.row(
        button_get_signatures,
    )
    return kb_builder.as_markup()
