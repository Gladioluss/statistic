import logging

from app.core.settings.app import AppSettings


class TestAppSettings(AppSettings):
    debug: bool = True

    title: str = "Test Defects"

    logging_level: int = logging.DEBUG

    class Config(AppSettings.Config):
        env_file = "test.env"
