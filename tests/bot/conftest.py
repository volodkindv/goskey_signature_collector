from contextlib import ExitStack
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

from src.bot.bot import get_bot, get_dispatcher, init_app
from src.bot.config_data.config import BotConfig, Config


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

    async def send_message(self, message: Message) -> None:
        update = Update(update_id=1, message=message)
        await self.dispatcher.feed_update(self.bot, update)

    async def send_callback(self, callback: CallbackQuery) -> None:
        update = Update(update_id=1, callback_query=callback)
        await self.dispatcher.feed_update(self.bot, update)

    def get_last_message_answer_args(self) -> MessageAnswerArgs:
        mock = Message.answer

        try:
            text = mock.call_args.args[0]
        except IndexError:
            text = mock.call_args.kwargs.get("text")
            # TODO научиться парсить сигнатуру метода в общем

        args = MessageAnswerArgs(text=text)
        args.reply_markup = mock.call_args.kwargs.get("reply_markup", None)

        return args

    def get_last_callback_edit_message_args(self) -> CallbackMessageEditTextArgs:
        mock = Message.edit_text
        text = mock.call_args.kwargs["text"]
        args = CallbackMessageEditTextArgs(text=text)
        args.reply_markup = mock.call_args.kwargs.get("reply_markup", None)

        return args

    def get_last_document_sent(self):
        mock = Message.answer_document
        document = mock.call_args.kwargs["document"]

        return document


@pytest.fixture(scope="session")
async def test_client(anyio_backend, test_client_mocks):
    test_config = Config(
        tg_bot=BotConfig(
            bot_token="111:AAA-bbb",
            database_uri="sqlite+aiosqlite:///",
            admin_user_ids="123,456",
        )
    )
    await init_app(test_config)

    yield TestClient(
        bot=get_bot(),
        dispatcher=get_dispatcher(),
    )


@pytest.fixture(scope="session")
def test_client_mocks(anyio_backend) -> None:
    to_patch = [
        (Message, "answer"),
        (Message, "edit_text"),
        (Message, "answer_document"),
        (CallbackQuery, "answer"),
    ]
    with ExitStack() as stack:
        for obj, attr in to_patch:
            stack.enter_context(patch.object(obj, attr, AsyncMock()))
        yield


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"
