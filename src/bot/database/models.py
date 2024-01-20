from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# declarative base class
class Base(DeclarativeBase):
    pass


# an example mapping using the base
class AppealModel(Base):
    __tablename__ = "appeal"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(100))
