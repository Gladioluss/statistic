from app.core.settings.app import AppSettings


class ProdAppSettings(AppSettings):

    title: str = "Prod Projects app"

    class Config(AppSettings.Config):
        env_file = "prod.env"
