from typing import Any

from pydantic import AnyHttpUrl, AnyUrl, PostgresDsn, validator

from app.core.settings.base import BaseAppSettings


class AppSettings(BaseAppSettings):
    API_PREFIX: str = "/api"
    API_TITLE: str
    CORS_ORIGINS: list[str] | list[AnyHttpUrl]
    OBJECT_AVAILABILITY_STATUS: str

    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: int | str
    DATABASE_NAME: str

    DB_POOL_SIZE: int = 90
    ASYNC_DATABASE_URI: PostgresDsn | None

    DATABASE_TEST_PORT: int | str
    ASYNC_DATABASE_URI_TEST: PostgresDsn | None

    SECRET_KEY: bytes

    RABBITMQ_URL: AnyUrl

    PROJECTS_QUEUE_NAME: str
    DEFECTS_QUEUE_NAME: str

    @validator("ASYNC_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: str | None, values: dict[str, Any]) -> Any:

        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("DATABASE_USER"),
            password=values.get("DATABASE_PASSWORD"),
            host=values.get("DATABASE_HOST"),
            port=str(values.get("DATABASE_PORT")),
            path=f"/{values.get('DATABASE_NAME') or ''}",
        )

    @validator("ASYNC_DATABASE_URI_TEST", pre=True)
    def assemble_db_test_connection(cls, v: str | None, values: dict[str, Any]) -> Any:

        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("DATABASE_USER"),
            password=values.get("DATABASE_PASSWORD"),
            host=values.get("DATABASE_HOST"),
            port=str(values.get("DATABASE_TEST_PORT")),
            path=f"/{values.get('DATABASE_NAME') or ''}_test",
        )

    class Config:
        case_sensitive = True
        validate_assignment = True
