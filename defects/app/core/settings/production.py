import logging

from app.core.settings.app import AppSettings


class ProdAppSettings(AppSettings):
    debug: bool = True

    title: str = "Prod Defects"

    logging_level: int = logging.DEBUG

    class Config(AppSettings.Config):
        env_file = "prod.env"
