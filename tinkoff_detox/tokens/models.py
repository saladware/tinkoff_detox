from uuid import UUID
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base


class Token(Base):
    __tablename__ = "token"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    user_id: Mapped[UUID]
    token: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str]
    created_at: Mapped[datetime]
