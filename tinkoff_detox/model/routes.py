from typing import Literal

from ..tokens.dependencies import TokenRequired

from fastapi import APIRouter, UploadFile


model = APIRouter()


@model.post("/textFilter")
async def text_filter(data: str, token: TokenRequired):
    return data


@model.post("/journalCommentsFilter")
async def journal_comments_filter(path: str, token: TokenRequired, type: Literal["blur", "rewrite"]):
    return path


@model.post("/audioFilter")
async def audio_filter(file: UploadFile, token: TokenRequired, type: Literal["blur", "rewrite"]):
    return file.file


@model.post("/videoFilter")
async def video_filter(file: UploadFile, token: TokenRequired, type: Literal["blur", "rewrite"]):
    return file.file
