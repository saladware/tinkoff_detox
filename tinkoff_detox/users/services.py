from abc import ABC, abstractmethod
from datetime import datetime, timedelta, timezone
from uuid import uuid4, UUID

from jose import jwt, JWTError
from passlib.context import CryptContext

from .models import User
from .exceptions import (
    UserAlreadyExistsException,
    AuthenticationException,
    UserNotFoundException,
)
from .repositories import BaseUsersRepository


class ITokenService(ABC):
    @abstractmethod
    def decode(self, token) -> dict | None:
        raise NotImplementedError

    @abstractmethod
    def encode(self, payload: dict) -> str:
        raise NotImplementedError


class JoseJWTService(ITokenService):
    def __init__(self, secret_key: str, algorithm: str) -> None:
        self.secret_key = secret_key
        self.algorithm = algorithm

    def decode(self, token) -> dict | None:
        try:
            return jwt.decode(token, self.secret_key, self.algorithm)
        except JWTError:
            return None

    def encode(self, payload: dict) -> str:
        data = payload.copy()
        return jwt.encode(data, self.secret_key, self.algorithm)


class IPasswordService(ABC):
    """interface of service for hashing and verifying passwords"""

    @abstractmethod
    def hash_password(self, password: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        raise NotImplementedError


class BcryptPasswordService(IPasswordService):
    """implementation of service for hashing and verifying passwords uses bcrypt algorithm"""

    context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        return self.context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.context.verify(plain_password, hashed_password)


class UserService:
    def __init__(
        self,
        repo: BaseUsersRepository,
        pwd_service: IPasswordService,
        jwt_service: ITokenService,
        access_token_expires_minutes: int,
    ):
        self.repo = repo
        self.pwd_service = pwd_service
        self.jwt_service = jwt_service
        self.access_token_expires_minutes = access_token_expires_minutes

    async def get_user_by_id(self, user_id: UUID) -> User:
        user = await self.repo.get_by_id(user_id)
        if user is None:
            raise UserNotFoundException(id=str(user_id))
        return user

    async def register_user(
        self, email: str, password: str, firstname: str, lastname: str
    ) -> User:
        user = await self.repo.get_by_email(email=email)
        if user is not None:
            raise UserAlreadyExistsException(email=email)
        user = User(
            id=uuid4(),
            email=email,
            hashed_password=self.pwd_service.hash_password(password),
            firstname=firstname,
            lastname=lastname,
            created_at=datetime.now(timezone.utc),
        )
        await self.repo.save(user)

        return user

    async def authenticate_user(self, email: str, password: str) -> User:
        user = await self.repo.get_by_email(email)
        if user is None or not self.pwd_service.verify_password(
            password, user.hashed_password
        ):
            raise AuthenticationException
        return user

    async def update_user(
        self,
        user: User,
        email: str | None = None,
        password: str | None = None,
        firstname: str | None = None,
        lastname: str | None = None,
    ):
        if email is not None:
            user_ = await self.repo.get_by_email(email)
            if user_ is not None:
                raise UserAlreadyExistsException(email=email)
        data = {
            "firstname": firstname,
            "lastname": lastname,
            "email": email,
            "hashed_password": (
                self.pwd_service.hash_password(password)
                if password is not None
                else None
            ),
        }

        for key, value in data.items():
            if value is not None:
                setattr(user, key, value)

        await self.repo.save(user)

    def create_access_token(self, user: User) -> str:
        payload = {
            "sub": str(user.id),
            "exp": datetime.now(timezone.utc)
            + timedelta(minutes=self.access_token_expires_minutes),
        }
        return self.jwt_service.encode(payload)

    async def get_user_by_access_token(self, token: str) -> User:
        payload = self.jwt_service.decode(token)
        if payload is None:
            raise AuthenticationException("token decode error")
        if payload["exp"] < int(datetime.now(timezone.utc).timestamp()):
            raise AuthenticationException("token expired")
        user = await self.repo.get_by_id(UUID(payload["sub"]))
        if user is None:
            raise AuthenticationException("token decode error")
        return user

    async def remove_user(self, user: User) -> None:
        await self.repo.remove(user)
        