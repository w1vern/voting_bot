
from enum import Enum
import os

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class BootLevel(str, Enum):
    DEBUG = "DEBUG"
    RELEASE = "RELEASE"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.getenv("ENV_FILE", "dev.env"),
        env_nested_delimiter="_",
        extra="ignore"
    )

    boot_level: BootLevel = BootLevel.DEBUG
    token: str = ""
    proxy: str | None = None

    @field_validator("proxy", mode="before")
    @classmethod
    def empty_str_to_none(cls, v: str | None) -> str | None:
        if v == "":
            return None
        return v


env_config = Settings()


if __name__ == "__main__":
    print(env_config.model_dump_json(indent=2))
