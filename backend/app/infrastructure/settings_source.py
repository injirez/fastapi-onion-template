import configparser

from typing import Any
from pathlib import Path

from pydantic.fields import FieldInfo
from pydantic_settings import PydanticBaseSettingsSource
from pydantic_settings.main import BaseSettings


class ConfigSettingsSource(PydanticBaseSettingsSource):
    def __init__(self, settings_cls: type[BaseSettings]):
        super().__init__(settings_cls)
        self.conf_setting = self._read_config()

    @staticmethod
    def _read_config():
        config = configparser.ConfigParser(allow_no_value=True, interpolation=None)
        project_dir = Path(__file__).resolve().parent.parent.parent.parent
        config.read(f"{project_dir}/app.conf", "utf-8")

        conf_setting = {
            "PORT_BACKEND": int(config.get("BASE", "PORT_BACKEND", fallback=8989)),
            "PORT_FRONTEND": int(config.get("BASE", "PORT_FRONTEND", fallback=80)),
            "SECRET_KEY": config.get("BASE", "SECRET_KEY", fallback=None),
            "JWT_ACCESS_EXPIRATION_SECONDS": int(config.get("BASE", "JWT_ACCESS_EXPIRATION_SECONDS", fallback=3600)),
        }
        return conf_setting

    def get_field_value(
        self,
        field: FieldInfo,
        field_name: str,
    ) -> tuple[Any, str, bool]:
        field_value = self.conf_setting.get(field_name)
        is_complex = isinstance(field_value, complex)
        return field_value, field_name, is_complex

    def prepare_field_value(
        self,
        field_name: str,
        field: FieldInfo,
        value: Any,
        value_is_complex: bool,
    ) -> Any:
        return value

    def __call__(self) -> dict[str, Any]:
        d: dict[str, Any] = {}

        for field_name, field in self.settings_cls.model_fields.items():
            field_value, field_key, value_is_complex = self.get_field_value(field, field_name)
            field_value = self.prepare_field_value(field_name, field, field_value, value_is_complex)
            if field_value is not None:
                d[field_key] = field_value

        return d
