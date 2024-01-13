import factory
from aiogram.types import CallbackQuery, Chat, Document, InaccessibleMessage, Message, User


class PrivateChatFactory(factory.Factory):
    class Meta:
        model = Chat

    type = "private"
    id = factory.Faker("pyint")


class MessageFactory(factory.Factory):
    class Meta:
        model = Message

    chat = factory.SubFactory(PrivateChatFactory)
    date = factory.Faker("date_object")  # лучше текущая дата/время
    message_id = factory.Faker("pyint")  # sequence лучше


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
    from_user: User = User(id=1, is_bot=False, first_name="Dan")
    message: Message | InaccessibleMessage | None = None
    """*Optional*. Message sent by the bot with the callback button that originated the query"""
    # inline_message_id: str|None = None
    data: str | None = None
