from typing import Annotated

from pydantic import (
    AnyHttpUrl,
    BaseModel,
    PostgresDsn,
    SecretStr,
    StringConstraints,
    field_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresConfig(BaseModel):
    URI: PostgresDsn
    # If set, sqlalchemy will print all the queries
    ECHO_QUERY: bool = False


class TokenConfig(BaseModel):
    EXPIRE_MINUTES: int


class LoggingConfig(BaseModel):
    # https://github.com/Delgan/loguru/blob/3d8631ef0015267ad68c5d65a250cb1aaa0b61fb/loguru/_defaults.py#L47
    LEVEL: Annotated[str, StringConstraints(to_upper=True)] = "INFO"
    SERIALIZE: bool = True


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_nested_delimiter="__",
        frozen=True,
        secrets_dir="/run/secrets",
    )
    # --- Project --- #

    PROJECT_NAME: str

    # --- Server --- #

    SERVER_NAME: str

    # ROOT_PREFIX is any prefix set by proxy, unaware to FastAPI.
    ROOT_PREFIX: str = "/api"

    # CORS_ORIGINS is a JSON-formatted list of origins
    # For eg. '["http://localhost", "http://localhost:3000", "http://localhost:8080"]'
    CORS_ORIGINS: list[AnyHttpUrl] | None = None

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: str | list[str] | None) -> str | list[str] | None:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        if isinstance(v, list | str):
            return v
        return v

    # Security
    SECRET_KEY: SecretStr

    # Database
    DATABASE: PostgresConfig

    # --- Configurations --- #

    # Tokens
    ACCESS_TOKEN: TokenConfig

    LOGGING: LoggingConfig = LoggingConfig()

    DEFAULT_REGION_CODE: str = "IN"


settings = Settings()
