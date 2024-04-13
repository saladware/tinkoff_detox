from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


class CreateToken(BaseModel):
    name: str


class TokenSchema(BaseModel):
    model_config = {
        "from_attributes": True
    }

    id: UUID
    name: str
    user_id: UUID
    created_at: datetime
