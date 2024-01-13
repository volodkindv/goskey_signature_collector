from functools import lru_cache

from pydantic import BaseModel


@lru_cache
def users_db() -> dict:
    return {}


class UserContext(BaseModel):
    pass


def get_user_context(user_id: str) -> UserContext:
    db = users_db()
    user_context = db.get(user_id)
    if not user_context:
        user_context = UserContext()
        db[user_id] = user_context
    return user_context
