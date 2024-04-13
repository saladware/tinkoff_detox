from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from abc import ABC, abstractmethod
from uuid import UUID
from .models import Token


class BaseTokensRepository(ABC):
    @abstractmethod
    async def get_by_id(self, token_id: UUID) -> Token | None:
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_token(self, value: str) -> Token | None:
        raise NotImplementedError

    @abstractmethod
    async def save(self, token: Token) -> None:
        raise NotImplementedError
    
    @abstractmethod
    async def remove(self, token: Token) -> None:
        raise NotImplementedError


class SqlalchemyTokensRepository(BaseTokensRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, token_id: UUID) -> Token | None:
        return await self.session.get(Token, token_id)

    async def save(self, token: Token) -> None:
        self.session.add(token)
        await self.session.commit()
        await self.session.refresh(token)
    
    async def remove(self, token: User) -> None:
        await self.session.delete(user)
        await self.session.commit()
    
    async def get_by_token(self, value: str) -> Token | None:
        query = select(Token).where(Token.email == email)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()


