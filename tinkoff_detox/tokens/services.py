from secrets import token_urlsafe

from uuid import uuid4, UUID
from datetime import datetime, timezone

from .repositories import BaseTokensRepository
from .models import Token
from ..users.models import User
from .exceptions import TokenNotFoundException


class TokensService:
    def __init__(self, repo: BaseTokensRepository) -> None:
        self.repo = repo

    async def create_token(self, name: str, by: User) -> Token:
        token = Token(
            id=uuid4(),
            user_id=by.id,
            token=token_urlsafe(32),
            name=name,
            created_at=datetime.now(timezone.utc),
        )
        await self.repo.save(token)
        return token

    async def get_by_id(self, token_id: UUID) -> Token:
        token = await self.repo.get_by_id(token_id)
        if token is None:
            raise TokenNotFoundException(id=str(token_id))
        return token

    async def check_token(self, value: str) -> bool:
        token = await self.repo.get_by_token(value)
        return token is not None
    
    async def get_token_by_value(self, value: str) -> Token:
        token = await self.repo.get_by_token(value)
        if token is None:
            raise TokenNotFoundException(value=value)
        return token

    async def get_all_users_tokens(self, user: User) -> list[Token]:
        return await self.repo.get_all(user_id=user.id)
    
    async def remove_token(self, token: Token, by: User) -> None:
        if token.user_id != by.id:
            raise TokenNotFoundException(id=str(token.id))
        await self.repo.remove(token)

