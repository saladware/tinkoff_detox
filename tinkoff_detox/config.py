from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgres+asyncpg:///db.sqlite3"

    