from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, Header, Security
from fastapi.security import APIKeyHeader

from .models import Token
from .services import TokensService
from .repositories import SqlalchemyTokensRepository
from ..database import get_database_session


def get_tokens_service(session: Annotated[AsyncSession, Depends(get_database_session)]) -> TokensService:
    return TokensService(repo=SqlalchemyTokensRepository(session=session))


Tokens = Annotated[TokensService, Depends(get_tokens_service)]


api_key_header = APIKeyHeader(name="X-API-Key")



async def get_api_token(x_token: Annotated[str, Security(api_key_header)], service: Tokens) -> Token:
    return await service.get_token_by_value(x_token)


TokenRequired = Annotated[Token, Depends(get_api_token)]