from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from abc import ABC, abstractmethod
from uuid import UUID
from .models import User


class BaseUsersRepository(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> User | None:
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        raise NotImplementedError
    
    @abstractmethod
    async def save(self, user: User) -> None:
        raise NotImplementedError
    
    @abstractmethod
    async def remove(self, user: User) -> None:
        raise NotImplementedError


class SqlalchemyUsersRepository(BaseUsersRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: UUID) -> User | None:
        return await self.session.get(User, user_id)

    async def save(self, user: User) -> None:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
    
    async def remove(self, user: User) -> None:
        await self.session.delete(user)
        await self.session.commit()
    
    async def get_by_email(self, email: str) -> User | None:
        query = select(User).where(User.email == email)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()


