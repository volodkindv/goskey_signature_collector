import pytest
from aiogram.types import Chat, User

from tests.bot.db_factories import AppealFactory

from .conftest import TestClient
from .factories import CallbackQueryFactory, DocumentFactory, MessageFactory, PrivateChatFactory, UserFactory

# This is the same as using the @pytest.mark.anyio on all test functions in the module
pytestmark = pytest.mark.anyio


@pytest.fixture
def admin_chat(test_client: TestClient) -> Chat:
    admin_user_id = 123
    chat = PrivateChatFactory(id=admin_user_id)
    yield chat


@pytest.fixture
def admin_user(test_client: TestClient) -> User:
    admin_user_id = 123
    chat = UserFactory(id=admin_user_id)
    yield chat


async def test_admin_menu(test_client: TestClient, admin_chat: Chat, admin_user: User):
    from src.bot.handlers.admin_handlers import admin_menu

    message = MessageFactory(text="/admin", chat=admin_chat, from_user=admin_user)
    await test_client.send_message(message)
    assert "Управление ботом" in test_client.get_last_message_answer_args().text


async def test_admin_appeals_list(test_client: TestClient, admin_chat: Chat, admin_user: User):
    from src.bot.handlers.admin_handlers import admin_appeals_list

    message = MessageFactory(text="/admin_appeals_list", chat=admin_chat, from_user=admin_user)
    await test_client.send_message(message)
    assert "Список инициатив (админка)" in test_client.get_last_message_answer_args().text


async def test_admin_appeals_add(test_client: TestClient, admin_chat: Chat, admin_user: User):
    from src.bot.handlers.admin_handlers import admin_appeals_add

    message = MessageFactory(text="/admin_appeals_add", chat=admin_chat, from_user=admin_user)
    await test_client.send_message(message)
    assert "Новая инициатива" in test_client.get_last_message_answer_args().text
    """
    Теперь ждем ввод: название инициативы; прикрепление файла; 
    В меню инициативы будет: опубликовать/снять; скачать подписи; приложить файл; изменить описание.
    """
