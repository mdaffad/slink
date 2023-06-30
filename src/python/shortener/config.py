from typing import List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, validator

DEFAULT_SQLALCHEMY_DATABASE_URI = PostgresDsn.build(
    scheme="postgresql+asyncpg",
    user="postgre",
    password="postgre",
    host="localhost",
    port="5432",
    path="/app",
)


class Settings(BaseSettings):
    PROJECT_NAME: str = "less"

    # POSTGRESQL DEFAULT DATABASE
    DEFAULT_DATABASE_SCHEME: str = "postgresql+asyncpg"
    DEFAULT_DATABASE_HOSTNAME: str = "localhost"
    DEFAULT_DATABASE_USER: str = "postgre"
    DEFAULT_DATABASE_PASSWORD: str = "postgre"
    DEFAULT_DATABASE_PORT: str = "5432"
    DEFAULT_DATABASE_DB: str = "app"
    DEFAULT_SQLALCHEMY_DATABASE_URI: str = ""

    # CORE SETTINGS
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []
    ALLOWED_HOSTS: list[str] = ["localhost", "127.0.0.1"]

    log_level: str = "DEBUG"

    @validator("log_level")
    def validate_log_level(cls, level: str, values: dict[str, str]):
        print("Here what you get")
        print(values)
        return level.upper()

    # VALIDATORS
    @validator("BACKEND_CORS_ORIGINS")
    def _assemble_cors_origins(cls, cors_origins: Union[str, List[AnyHttpUrl]]):
        if isinstance(cors_origins, str):
            return [item.strip() for item in cors_origins.split(",")]
        return cors_origins

    @validator("DEFAULT_SQLALCHEMY_DATABASE_URI")
    def _assemble_default_db_connection(
        cls, v: str, values: dict[str, Optional[str]]
    ) -> str:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values["DEFAULT_DATABASE_USER"],
            password=values["DEFAULT_DATABASE_PASSWORD"],
            host=values["DEFAULT_DATABASE_HOSTNAME"],
            port=values["DEFAULT_DATABASE_PORT"],
            path=f"/{values['DEFAULT_DATABASE_DB']}",
        )


settings = Settings()
