from .exceptions import (
    ItemAccessDeniedException,
    ItemAlreadyExistsException,
    ItemException,
    ItemNotFoundException,
)
from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import ORJSONResponse
from starlette.types import ASGIApp

from .users.routes import users
from .tokens.routes import tokens
from .model.routes import model


async def item_exception_handler(request: Request, exception: Exception) -> Response:
    """
    A coroutine that handles exceptions for specific item-related exceptions and maps them to appropriate HTTP status codes.
    """

    codes_mapping = {
        ItemNotFoundException: status.HTTP_404_NOT_FOUND,
        ItemAlreadyExistsException: status.HTTP_409_CONFLICT,
        ItemAccessDeniedException: status.HTTP_403_FORBIDDEN,
    }

    for key, status_code in codes_mapping.items():
        if isinstance(exception, key):
            return ORJSONResponse(
                status_code=status_code, content={"detail": exception.message}
            )
    return await http_exception_handler(
        request=request,
        exc=HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="unknown error"
        ),
    )


def get_app() -> ASGIApp:
    app = FastAPI(
        title="Tinkoff Detox API",
        description="API для фильтрации токсичного контента",
        version="1.0.0",
    )

    app.include_router(users, prefix="/users", tags=["users"])
    app.include_router(tokens, prefix="/tokens", tags=["tokens"])
    app.include_router(model, prefix="/model", tags=["model"])
    app.add_exception_handler(ItemException, item_exception_handler)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost",
            "http://localhost:8000",
            "http://localhost:3000",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
