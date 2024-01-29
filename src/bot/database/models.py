from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class AppealModel(Base):
    __tablename__ = "appeal"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(100))
    is_hidden: Mapped[bool] = mapped_column(Boolean, default=True)
    file_id: Mapped[str] = mapped_column(String(255), nullable=True)
    file_name: Mapped[str] = mapped_column(String(255), nullable=True)


class UserModel(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(100))


class UserSignatureModel(Base):
    __tablename__ = "user_signature"

    id: Mapped[int] = mapped_column(primary_key=True)

    appeal_id = mapped_column(ForeignKey("appeal.id"))
    appeal = relationship("AppealModel")

    user_id = mapped_column(ForeignKey("user.id"))
    user = relationship("UserModel")

    file_id: Mapped[str] = mapped_column(String(255), nullable=True)
    file_name: Mapped[str] = mapped_column(String(255), nullable=True)
