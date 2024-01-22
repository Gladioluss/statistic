from contextlib import asynccontextmanager

import pytest
import pytest_asyncio
from alembic.command import upgrade
from alembic.config import Config
from loguru import logger

from app.api.v1.api import api_router_v1
from app.core.config import settings
from app.core.rabbit.rabbit_connection import rabbit_connection
from fastapi import FastAPI
from fastapi_async_sqlalchemy import SQLAlchemyMiddleware
from httpx import AsyncClient
from prometheus_fastapi_instrumentator import Instrumentator
from sqlmodel import Session, SQLModel, create_engine
from starlette.middleware.cors import CORSMiddleware


@pytest.fixture(scope='session', autouse=True)
def migrate_test_db():
    alembic_config = Config('tests/alembic.ini')
    upgrade(alembic_config, 'head')


@pytest.fixture
def db():
    engine = create_engine(settings.ASYNC_DATABASE_URI_TEST)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)


@pytest.fixture
def app() -> FastAPI:
    logger.info(settings.ASYNC_DATABASE_URI_TEST)
    @asynccontextmanager
    async def lifespan(_: FastAPI):
        await rabbit_connection.connect()
        yield
        await rabbit_connection.disconnect()

    app = FastAPI(title=settings.API_TITLE, lifespan=lifespan)
    app.include_router(api_router_v1, prefix=settings.API_PREFIX)

    app.add_middleware(
        SQLAlchemyMiddleware,
        db_url=settings.ASYNC_DATABASE_URI_TEST,
        engine_args={
            "echo": False,
            "pool_pre_ping": True,
            "pool_size": settings.DB_POOL_SIZE,
            "max_overflow": 64,
        }
    )

    if settings.CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    Instrumentator().instrument(app).expose(app)
    return app


@pytest_asyncio.fixture
async def client(app: FastAPI) -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        yield ac
