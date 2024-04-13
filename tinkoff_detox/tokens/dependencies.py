from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, Header

from .models import Token
from .services import TokensService
from .repositories import SqlalchemyTokensRepository
from ..database import get_database_session


def get_tokens_service(session: Annotated[AsyncSession, Depends(get_database_session)]) -> TokensService:
    return TokensService(repo=SqlalchemyTokensRepository(session=session))


Tokens = Annotated[TokensService, Depends(get_tokens_service)]


async def get_api_token(authorization: Annotated[str, Header()], service: Tokens) -> Token:
    return await service.get_token_by_value(authorization)


TokenRequired = Annotated[Token, Depends(get_api_token)]