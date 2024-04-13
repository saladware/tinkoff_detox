from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


if TYPE_CHECKING:
    from ..tokens.models import Token


class User(Base):
    __tablename__ = "user"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    firstname: Mapped[str]
    lastname: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    created_at: Mapped[datetime]
    tokens: Mapped[list["Token"]] = relationship(back_populates="user", cascade="all, delete, delete-orphan")
