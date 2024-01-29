from __future__ import annotations

import factory
from aiogram.types import CallbackQuery, Chat, Document, InaccessibleMessage, Message, User


class UserFactory(factory.Factory):
    class Meta:
        model = User

    id: int = factory.Faker("pyint")
    is_bot: bool = False
    first_name: str = factory.Faker("name")


class PrivateChatFactory(factory.Factory):
    class Meta:
        model = Chat

    type = "private"
    id = factory.Faker("pyint")
    username = factory.Faker("name")


class MessageFactory(factory.Factory):
    class Meta:
        model = Message

    chat = factory.SubFactory(PrivateChatFactory)
    date = factory.Faker("date_object")  # лучше текущая дата/время
    message_id = factory.Faker("pyint")  # sequence лучше
    from_user = factory.SubFactory(UserFactory)


class DocumentFactory(factory.Factory):
    class Meta:
        model = Document

    file_id = factory.Faker("uuid4")
    file_unique_id = factory.Faker("uuid4")


class CallbackQueryFactory(factory.Factory):
    class Meta:
        model = CallbackQuery

    id: str = "123"
    chat_instance: str = "123"
    from_user: User = factory.SubFactory(UserFactory)
    message: Message | InaccessibleMessage | None = None
    """*Optional*. Message sent by the bot with the callback button that originated the query"""
    # inline_message_id: str|None = None
    data: str | None = None
