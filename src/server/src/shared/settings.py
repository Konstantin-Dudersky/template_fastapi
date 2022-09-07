"""Файл для настроек.

Для чтения настроек импортировать:
from src.utils.settings import settings

Для создания файла с дефолтными настройками запустить функцию create_env():
poetry run poe create_env
"""


from dotenv import set_key  # pyright: ignore[reportUnknownVariableType]

from pydantic import AnyUrl, BaseSettings, Field, PostgresDsn

ENV_FILE: str = ".env"
ENCODING: str = "utf-8"


class Settings(BaseSettings):
    """Модель для сохранения настроек."""

    class Config(BaseSettings.Config):
        """Настройки."""

        env_file: str = ENV_FILE
        env_file_encoding: str = ENCODING

    debug: bool = False
    db_data_url: PostgresDsn = Field(
        default="postgresql://postgres:postgres@10.101.80.140:5432/energy_data",
    )
    db_conf_url: PostgresDsn = Field(
        default="postgresql://postgres:postgres@10.101.80.140:5432/energy_conf",
    )
    plc_url: AnyUrl = Field(default="opc.tcp://192.168.10.20:4840")
    scanner_port: str = "/dev/ttyACM0"
    telegram_token: str = "5422079866:AAFarQ9FrwDRj08k73e5JB-e9eSag020iqQ"
    telegram_chat_id: str = "-1001555100085"


def create_env() -> None:
    """Записывает файл с дефолтными значениями."""
    for key, value in Settings().dict().items():
        set_key(
            dotenv_path=ENV_FILE,
            key_to_set=key,
            value_to_set=value,
            quote_mode="never",
            export=False,
            encoding=ENCODING,
        )


settings: Settings = Settings()

if __name__ == "__main__":
    pass
