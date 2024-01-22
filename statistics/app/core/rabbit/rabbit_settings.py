from functools import lru_cache

from pydantic import BaseSettings

from app.core.config import settings


class RabbitServerSettings(BaseSettings):
    rabbit_url: str = settings.RABBITMQ_URL


class ProjectQueueReceive(RabbitServerSettings):
    queue: str = settings.PROJECTS_QUEUE_NAME
    auto_delete: bool = False
    durable: bool = True


class DefectsQueueReceive(RabbitServerSettings):
    queue: str = settings.DEFECTS_QUEUE_NAME
    auto_delete: bool = False
    durable: bool = True


class RabbitSettings:
    basic = RabbitServerSettings()
    projects = ProjectQueueReceive()
    defects = DefectsQueueReceive()

@lru_cache
def get_rmq_settings() -> RabbitSettings:
    return RabbitSettings()


rmq_settings = get_rmq_settings()
