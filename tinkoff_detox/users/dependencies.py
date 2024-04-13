from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from .services import UserService, BcryptPasswordService, JoseJWTService
from .repositories import SqlalchemyUsersRepository
from ..database import get_database_session
from ..config import get_settings, Settings
from .exceptions import AuthenticationException
from .models import User


def get_user_service(
    session: Annotated[AsyncSession, Depends(get_database_session)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> UserService:
    return UserService(
        repo=SqlalchemyUsersRepository(session),
        pwd_service=BcryptPasswordService(),
        jwt_service=JoseJWTService(
            settings.access_token_secret_key, settings.access_token_algorithm
        ),
        access_token_expires_minutes=settings.access_token_expires_minutes,
    )


Users = Annotated[UserService, Depends(get_user_service)]


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


async def get_current_user(
    service: Users, token: Annotated[str, Depends(oauth2_scheme)]
):
    try:
        return await service.get_user_by_access_token(token=token)
    except AuthenticationException as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc.message),
        )


Me = Annotated[User, Depends(get_current_user)]

LoginForm = Annotated[OAuth2PasswordRequestForm, Depends()]
