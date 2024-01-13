from functools import lru_cache

from ..schemas.schemas import Appeal, UserContext


@lru_cache
def users_db() -> dict:
    return {}


def get_user_context(user_id: str) -> UserContext:
    db = users_db()
    user_context = db.get(user_id)
    if not user_context:
        user_context = UserContext()
        db[user_id] = user_context
    return user_context


async def get_current_appeals() -> list[Appeal]:
    count = 5
    return [
        Appeal(
            id=counter,
            name=f"Сбор подписей {counter}",
        )
        for counter in range(count)
    ]
