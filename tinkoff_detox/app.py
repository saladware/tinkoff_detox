from fastapi import FastAPI
from starlette.types import ASGIApp

def get_app() -> ASGIApp:
    app = FastAPI(
        title="tinkoff_detox",
        version="1.0.0",
        description="tinkoff_detox",
    )

    return app
