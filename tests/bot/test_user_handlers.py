import pytest

from tests.bot.db_factories import AppealFactory

from .conftest import TestClient
from .factories import CallbackQueryFactory, DocumentFactory, MessageFactory, PrivateChatFactory, UserFactory

# This is the same as using the @pytest.mark.anyio on all test functions in the module
pytestmark = pytest.mark.anyio


async def test_help(test_client: TestClient):
    from src.bot.handlers.common_handlers import process_help_command

    message = MessageFactory(text="/help")
    await test_client.send_message(message)
    assert "Бот, помогающий в сборе подписей" in test_client.get_last_message_answer_args().text
    assert "Доступные команды" in test_client.get_last_message_answer_args().text


async def test_start(test_client: TestClient):
    from src.bot.handlers.common_handlers import process_start_command

    message = MessageFactory(text="/start")
    await test_client.send_message(message)
    assert "Бот, помогающий в сборе подписей" in test_client.get_last_message_answer_args().text
    assert "Доступные команды" in test_client.get_last_message_answer_args().text


async def test_appeals_list(test_client: TestClient):
    from src.bot.handlers.user_handlers import process_appeals_list_command

    appeal = await AppealFactory.create_async()

    message = MessageFactory(text="/appeals")
    await test_client.send_message(message)
    assert appeal.text in test_client.get_last_message_answer_args().text


async def test_appeals_item_exists(test_client: TestClient):
    from src.bot.handlers.user_handlers import process_appeals_item_command

    appeal = await AppealFactory.create_async()
    message = MessageFactory(text=f"/appeals_{appeal.id}")
    await test_client.send_message(message)
    args = test_client.get_last_message_answer_args()
    assert appeal.text in args.text
    assert args.reply_markup.inline_keyboard


async def test_scenario(test_client: TestClient):
    """Сквозной диалог"""

    chat = PrivateChatFactory()

    message = MessageFactory(text="/start", chat=chat)
    await test_client.send_message(message)
    assert "Бот" in test_client.get_last_message_answer_args().text

    message = MessageFactory(text="/appeals", chat=chat)
    await test_client.send_message(message)
    assert "Список инициатив" in test_client.get_last_message_answer_args().text

    appeal = await AppealFactory.create_async()
    message = MessageFactory(text=f"/appeals_{appeal.id}")
    await test_client.send_message(message)
    assert appeal.text in test_client.get_last_message_answer_args().text


async def test_appeals_item_press_manual(test_client: TestClient):
    from src.bot.handlers.user_handlers import process_appeal_manual_cb, process_appeals_item_command

    message = MessageFactory(text="/appeals_1")
    await test_client.send_message(message)
    # TODO вынести шаг перехода к инициативе в фикстуру

    cb = CallbackQueryFactory(message=message, data="Инструкция")
    await test_client.send_callback(cb)
    assert "Инструкция" in test_client.get_last_message_answer_args().text


async def test_appeals_item_press_sign(test_client: TestClient):
    from src.bot.handlers.user_handlers import process_appeal_send_cb, process_appeals_item_command

    user = UserFactory()
    chat = PrivateChatFactory(id=user.id)

    appeal = await AppealFactory.create_async()
    message = MessageFactory(text=f"/appeals_{appeal.id}", from_user=user, chat=chat)
    await test_client.send_message(message)
    args = test_client.get_last_message_answer_args()
    assert appeal.text in args.text

    # теперь отправить callback
    cb = CallbackQueryFactory(message=message, data="Подписать", from_user=user)
    await test_client.send_callback(cb)
    assert "Ознакомьтесь" in test_client.get_last_message_answer_args().text
    assert test_client.get_last_document_sent()
    # TODO проверить


async def test_proсess_file_received(test_client: TestClient):
    from src.bot.handlers.user_handlers import process_file_received

    user = UserFactory()
    chat = PrivateChatFactory(id=user.id)

    appeal = await AppealFactory.create_async()
    message = MessageFactory(text=f"/appeals_{appeal.id}", from_user=user, chat=chat)
    await test_client.send_message(message)
    # TODO вынести шаг перехода к инициативе в фикстуру

    cb = CallbackQueryFactory(message=message, data="Подписать", from_user=user)
    await test_client.send_callback(cb)

    # теперь отправляем файл
    doc = DocumentFactory()
    message = MessageFactory(document=doc, from_user=user, chat=chat)
    await test_client.send_message(message)
    assert "Спасибо" in test_client.get_last_message_answer_args().text
