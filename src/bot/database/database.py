from sqlalchemy import select

from ..context import GlobalContext
from ..schemas.schemas import Appeal
from .models import AppealModel, Base


async def init_models() -> None:
    async with GlobalContext.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_appeals() -> list[AppealModel]:
    async with GlobalContext.async_session() as session:
        query = await session.execute(select(AppealModel).limit(20))
        return query.scalars().all()


async def get_current_appeals() -> list[Appeal]:
    appeals = await get_appeals()
    return [
        Appeal(
            id=appeal.id,
            name=appeal.text,
        )
        for appeal in appeals
    ]
