from unittest.mock import AsyncMock, patch

import pytest
from aiogram import Bot, Dispatcher
from aiogram.types import (
    CallbackQuery,
    ForceReply,
    InlineKeyboardMarkup,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
)
from pydantic import BaseModel, ConfigDict

from src.bot.bot import get_bot, get_dispatcher


class MessageAnswerArgs(BaseModel):
    text: str
    reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply | None = None


class CallbackMessageEditTextArgs(BaseModel):
    text: str
    reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply | None = None


class TestClient(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    bot: Bot
    dispatcher: Dispatcher
    message_answer_mock: AsyncMock
    message_edit_text_mock: AsyncMock
    callback_answer_mock: AsyncMock
    answer_document_mock: AsyncMock
    # реализовать его как контекстный менеджер, чтоб он сам патчил

    async def send_message(self, message: Message) -> None:
        update = Update(update_id=1, message=message)
        await self.dispatcher.feed_update(self.bot, update)

    async def send_callback(self, callback: CallbackQuery) -> None:
        update = Update(update_id=1, callback_query=callback)
        await self.dispatcher.feed_update(self.bot, update)

    def get_last_message_answer_args(self) -> MessageAnswerArgs:
        try:
            text = self.message_answer_mock.call_args.args[0]
        except IndexError:
            text = self.message_answer_mock.call_args.kwargs.get("text")

        args = MessageAnswerArgs(text=text)
        args.reply_markup = self.message_answer_mock.call_args.kwargs.get("reply_markup", None)

        return args

    def get_last_callback_edit_message_args(self) -> CallbackMessageEditTextArgs:
        text = self.message_edit_text_mock.call_args.kwargs["text"]
        args = CallbackMessageEditTextArgs(text=text)
        args.reply_markup = self.message_answer_mock.call_args.kwargs.get("reply_markup", None)

        return args

    def get_last_document_sent(self):
        document = self.answer_document_mock.call_args.kwargs["document"]

        return document


@pytest.fixture(scope="session")
def test_client(anyio_backend):
    fake_token = "111:AAA-bbb"
    bot = get_bot(bot_token=fake_token)
    dispatcher = get_dispatcher()

    with patch.object(Message, "answer", AsyncMock()) as answer_mock:
        with patch.object(Message, "edit_text", AsyncMock()) as edit_text_mock:
            with patch.object(CallbackQuery, "answer", AsyncMock()) as callback_answer_mock:
                with patch.object(Message, "answer_document", AsyncMock()) as answer_document_mock:
                    yield TestClient(
                        bot=bot,
                        dispatcher=dispatcher,
                        message_answer_mock=answer_mock,
                        message_edit_text_mock=edit_text_mock,
                        callback_answer_mock=callback_answer_mock,
                        answer_document_mock=answer_document_mock,
                    )


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"
