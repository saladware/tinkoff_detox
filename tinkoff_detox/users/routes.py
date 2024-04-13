from typing import Literal
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from ..users.dependencies import LoginForm, Me, Users
from ..users.exceptions import AuthenticationException
from ..users.schemas import CreateUser, Token, UpdateUser, UserPrivate, UserPublic


users = APIRouter()


@users.get("/me", response_model=UserPrivate)
async def get_me(user: Me):
    return user


@users.patch("/me", response_model=UserPrivate)
async def update_user(data: UpdateUser, user: Me, service: Users):
    await service.update_user(user=user, **data.model_dump(exclude_none=True))
    return user


@users.delete("/me", response_model=Literal["done"])
async def remove_user(user: Me, service: Users):
    await service.remove_user(user=user)
    return "done"


@users.get("/{user_id}", response_model=UserPublic)
async def get_user(user_id: UUID, service: Users):
    return await service.get_user_by_id(user_id)


@users.post("/", response_model=UserPrivate)
async def register_user(data: CreateUser, service: Users):
    return await service.register_user(
        email=data.email,
        password=data.password,
        firstname=data.firstname,
        lastname=data.lastname,
    )


@users.post("/login", response_model=Token)
async def login(form_data: LoginForm, service: Users):
    try:
        user = await service.authenticate_user(
            email=form_data.username, password=form_data.password
        )
    except AuthenticationException as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=exc.message,
        ) from exc
    return {
        "access_token": service.create_access_token(user),
        "token_type": "bearer",
    }
