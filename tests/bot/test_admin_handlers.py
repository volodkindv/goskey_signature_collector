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


async def test_ping_admin(test_client: TestClient, admin_chat: Chat, admin_user: User):
    from src.bot.handlers.admin_handlers import ping_admin

    message = MessageFactory(text="/ping_admin", chat=admin_chat, from_user=admin_user)
    await test_client.send_message(message)
    assert "ping" in test_client.get_last_message_answer_args().text
