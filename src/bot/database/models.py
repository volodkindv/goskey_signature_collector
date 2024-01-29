from sqlalchemy import Boolean, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class AppealModel(Base):
    __tablename__ = "appeal"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(100))
    is_hidden: Mapped[bool] = mapped_column(Boolean, default=True)
