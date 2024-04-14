from typing import Literal

from ..tokens.dependencies import TokenRequired

from fastapi import APIRouter, UploadFile

from .ml import detoxify
from .parser import get_comments_by_article


model = APIRouter()


@model.post("/textFilter")
def text_filter(
    promt: str,
    token: TokenRequired,
    max_tokens: int = 50,
    temperature: float = 0.7,
    top_k: int = 50,
    top_p: float = 0.95,
    penalty: float = 1.0,
    n: int = 1,
):
    return detoxify(promt, max_tokens, temperature, top_k, top_p, penalty, n)


@model.post("/journalCommentsFilter")
def journal_comments_filter(
    path: str,
    token: TokenRequired,
    offset: int = 0,
    limit: int = 10,
    max_tokens: int = 50,
    temperature: float = 0.7,
    top_k: int = 50,
    top_p: float = 0.95,
    penalty: float = 1.0,
    n: int = 1,
):
    comments = get_comments_by_article(path)
    return [
        {
            "promt": comment,
            "result": detoxify(comment, max_tokens, temperature, top_k, top_p, penalty, n)
        }
        for comment in comments
    ]
        



@model.post("/audioFilter")
async def audio_filter(
    file: UploadFile,
    token: TokenRequired,
    max_tokens: int = 50,
    temperature: float = 0.7,
    top_k: int = 50,
    top_p: float = 0.95,
    penalty: float = 1.0,
    n: int = 1,
):
    return file.file


@model.post("/videoFilter")
async def video_filter(
    file: UploadFile, token: TokenRequired, type: Literal["blur", "rewrite"]
):
    return file.file
