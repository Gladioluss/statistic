from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_async_sqlalchemy import SQLAlchemyMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router_v1
from app.core.config import settings
from app.core.rabbit.rabbit_connection import rabbit_connection


@asynccontextmanager
async def lifespan(_: FastAPI):
    await rabbit_connection.connect()
    yield
    await rabbit_connection.disconnect()

app = FastAPI(title=settings.API_TITLE, lifespan=lifespan)
app.include_router(api_router_v1, prefix=settings.API_PREFIX)

app.add_middleware(
    SQLAlchemyMiddleware,
    db_url=settings.ASYNC_DATABASE_URI,
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
