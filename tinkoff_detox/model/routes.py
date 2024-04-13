from ..tokens.dependencies import TokenRequired

from fastapi import APIRouter


model = APIRouter()


@model.post("/textFilter")
async def text_filter(data: str, token: TokenRequired):
    return data
