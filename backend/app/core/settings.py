from pathlib import Path

from functools import cached_property

from pydantic import computed_field
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource

from infrastructure.settings_source import ConfigSettingsSource


class Settings(BaseSettings):
    DEBUG_MODE: bool = True
    BASE_PATH: Path = Path(__file__).resolve().parent.parent
    CONFIG_FILE: Path = Path(__file__).resolve().parent.parent.parent.parent / "app.conf"
    URL_DATABASE: str = f"sqlite+aiosqlite:///{BASE_PATH.parent}/database.db"
    JWT_ALGORITHM: str = "HS256"

    PORT_BACKEND: int
    PORT_FRONTEND: int
    SECRET_KEY: str
    JWT_ACCESS_EXPIRATION_SECONDS: int

    @computed_field
    @cached_property
    def LOG_PATH(self) -> str:  # noqa: N802
        return "/var/log/fatapi-onion-template.log"

    @computed_field
    @cached_property
    def UVICORN_LOG_PATH(self) -> str:  # noqa: N802
        return str(self.BASE_PATH.parent / "logging.json")

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """app.conf handler"""
        return (
            init_settings,
            ConfigSettingsSource(settings_cls),
            env_settings,
            dotenv_settings,
            file_secret_settings,
        )

    @computed_field
    @cached_property
    def LOGGER_CONFIG(self) -> dict:
        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "verbose": {
                    "format": "[%(asctime)s] %(levelname)s %(message)s %(exc_info)s",
                },
            },
            "handlers": {
                "default": {
                    "level": "INFO",
                    "formatter": "verbose",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout",  # Default is stderr
                },
                "file": {
                    "level": "INFO",
                    "class": "logging.FileHandler",
                    "filename": self.LOG_PATH,
                    "formatter": "verbose",
                },
            },
            "loggers": {
                "server": {
                    "handlers": ["file", "default"],
                    "level": "INFO",
                    "propagate": True,
                },
                "uvicorn.error": {
                    "level": "DEBUG",
                    "handlers": ["default", "file"],
                },
                "uvicorn.access": {
                    "level": "DEBUG",
                    "handlers": ["default", "file"],
                },
            },
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }


settings = Settings()  # type: ignore
