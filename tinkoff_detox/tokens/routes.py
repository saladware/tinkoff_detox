from typing import Literal
from uuid import UUID

from fastapi import APIRouter

from ..users.dependencies import Me
from .dependencies import Tokens
from .schemas import TokenSchema, CreateToken


tokens = APIRouter()


@tokens.get("/", response_model=list[TokenSchema])
async def get_tokens(user: Me, tokens: Tokens):
    return await tokens.get_all_users_tokens(user=user)


@tokens.post("/", response_model=TokenSchema)
async def create_token(data: CreateToken, user: Me, tokens: Tokens):
    return await tokens.create_token(name=data.name, by=user)


@tokens.delete("/{token_id}", response_model=Literal["done"])
async def remove_token(token_id: UUID, user: Me, tokens: Tokens):
    token = await tokens.get_by_id(token_id)
    await tokens.remove_token(token=token, by=user)
    return "done"