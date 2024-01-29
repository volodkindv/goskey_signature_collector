from sqlalchemy import select

from ..context import GlobalContext
from .models import AppealModel, Base, UserModel, UserSignatureModel


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


async def change_appeal_text(appeal_id: str, new_text: str) -> AppealModel | None:
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


async def change_appeal_file(appeal_id: str, new_file_id: str, new_file_name: str) -> AppealModel | None:
    async with GlobalContext.async_session() as session:
        query_text = select(AppealModel).filter(AppealModel.id == appeal_id)
        query = await session.execute(query_text)
        appeal = query.scalars().first()  # TODO None
        appeal.file_id = new_file_id
        appeal.file_name = new_file_name
        await session.commit()
        return appeal


async def create_appeal(text: str = "Новая инициатива") -> AppealModel:
    async with GlobalContext.async_session() as session:
        new_appeal = AppealModel(text=text)
        session.add(new_appeal)
        await session.commit()
    return new_appeal


async def post_user_signature(
    user: UserModel,
    appeal: AppealModel,
    file_id: str,
    file_name: str,
) -> UserSignatureModel:
    async with GlobalContext.async_session() as session:
        query_text = select(UserSignatureModel).filter(
            UserSignatureModel.user == user,
            UserSignatureModel.appeal == appeal,
        )
        query = await session.execute(query_text)
        signature = query.scalars().first()
        if signature is None:
            signature = UserSignatureModel(user=user, appeal=appeal)
            session.add(signature)

        signature.file_id = file_id
        signature.file_name = file_name
        await session.commit()
        return signature


async def get_or_create_user(user_id: int, user_name: str) -> UserModel:
    async with GlobalContext.async_session() as session:
        query_text = select(UserModel).filter(UserModel.id == user_id)
        query = await session.execute(query_text)
        user = query.scalars().first()
        if user is None:
            user = UserModel(name=user_name, user_id=user_id)
            session.add(user)
            await session.commit()
        return user
