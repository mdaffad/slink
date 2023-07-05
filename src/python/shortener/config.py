import json
from typing import List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, SecretStr, validator


class Settings(BaseSettings):
    PROJECT_NAME: str = "shortener"

    # POSTGRESQL DATABASE
    DATABASE_SCHEME: str = "postgresql+asyncpg"
    DATABASE_HOSTNAME: str = "localhost"
    DATABASE_USER: str = "postgre"
    DATABASE_PASSWORD: str = "postgre"
    DATABASE_PORT: str = "5432"
    DATABASE_DB: str = "app"
    SQLALCHEMY_DATABASE_URI: str = ""

    # KAFKA PUBLISHER
    PUBLISHER_DEST_HOST: str = "localhost:9092"

    # CORE SETTINGS
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []
    ALLOWED_HOSTS: list[str] = ["localhost", "127.0.0.1"]

    # BASIC AUTH SETTINGS
    BASIC_AUTH_USERNAME: SecretStr = "admin"
    BASIC_AUTH_PASSWORD: SecretStr = "admin123"

    LOG_LEVEL: str = "DEBUG"

    class Config:
        env_prefix = "SHORTENER_"

    @validator("LOG_LEVEL")
    def validate_log_level(cls, level: str, values: dict[str, str]):
        SecretStr.get_secret_value
        pretty = json.dumps(values, indent=4, default=lambda obj: obj.__str__())
        print(pretty)
        return level.upper()

    # VALIDATORS
    @validator("BACKEND_CORS_ORIGINS")
    def _assemble_cors_origins(cls, cors_origins: Union[str, List[AnyHttpUrl]]):
        if isinstance(cors_origins, str):
            return [item.strip() for item in cors_origins.split(",")]
        return cors_origins

    @validator("SQLALCHEMY_DATABASE_URI")
    def _assemble_db_connection(cls, _: str, values: dict[str, Optional[str]]) -> str:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values["DATABASE_USER"],
            password=values["DATABASE_PASSWORD"],
            host=values["DATABASE_HOSTNAME"],
            port=values["DATABASE_PORT"],
            path=f"/{values['DATABASE_DB']}",
        )


settings = Settings()
