from polyfactory import Ignore
from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory

from src.bot.context import GlobalContext
from src.bot.database.models import AppealModel


class AppealFactory(SQLAlchemyFactory[AppealModel]):
    __async_session__ = GlobalContext.get_session
    id = Ignore()
    is_hidden = False
