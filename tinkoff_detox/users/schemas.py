from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, EmailStr


class CreateUser(BaseModel):
    email: EmailStr
    password: str
    firstname: str
    lastname: str


class UserPublic(BaseModel):
    model_config = {
        "from_attributes": True
    }

    id: UUID
    firstname: str
    lastname: str
 

class UserPrivate(BaseModel):
    model_config = {
        "from_attributes": True
    }
    id: UUID
    email: str
    firstname: str
    lastname: str
    created_at: datetime


class UpdateUser(BaseModel):
    email: EmailStr | None = None
    password: str | None = None
    firstname: str | None = None
    lastname: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str
