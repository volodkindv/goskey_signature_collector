from sqlalchemy import select

from ..context import GlobalContext
from .models import AppealModel, Base


async def init_models() -> None:
    async with GlobalContext.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_appeals(show_hidden: bool = False) -> list[AppealModel]:
    async with GlobalContext.async_session() as session:
        query_text = select(AppealModel).limit(20)
        if not show_hidden:
            query_text = query_text.filter(AppealModel.is_hidden == False)  # noqa: E712

        query = await session.execute(query_text)
        return query.scalars().all()


async def get_appeal(appeal_id: str) -> AppealModel | None:
    async with GlobalContext.async_session() as session:
        query_text = select(AppealModel).filter(AppealModel.id == appeal_id)
        query = await session.execute(query_text)
        return query.scalars().first()


async def edit_appeal(appeal_id: str, new_text: str) -> AppealModel | None:
    async with GlobalContext.async_session() as session:
        query_text = select(AppealModel).filter(AppealModel.id == appeal_id)
        query = await session.execute(query_text)
        appeal = query.scalars().first()  # TODO None
        appeal.text = new_text
        await session.commit()
        return appeal


async def change_appeal_visibility(appeal_id: str, is_hidden: bool) -> AppealModel | None:
    async with GlobalContext.async_session() as session:
        query_text = select(AppealModel).filter(AppealModel.id == appeal_id)
        query = await session.execute(query_text)
        appeal = query.scalars().first()  # TODO None
        appeal.is_hidden = is_hidden
        await session.commit()
        return appeal


async def create_appeal(text: str = "Новая инициатива") -> AppealModel:
    async with GlobalContext.async_session() as session:
        new_appeal = AppealModel(text=text)
        session.add(new_appeal)
        await session.commit()
    return new_appeal
