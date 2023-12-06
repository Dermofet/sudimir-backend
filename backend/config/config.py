from __future__ import annotations

from functools import lru_cache
from typing import Any, Dict, Optional

from dotenv import find_dotenv

from pydantic import Field, PostgresDsn, field_validator
from pydantic_settings import SettingsConfigDict, BaseSettings
from pydantic_core.core_schema import FieldValidationInfo


class AsyncPostgresDsn(PostgresDsn):
    allowed_schemes = {"postgres+asyncpg", "postgresql+asyncpg"}


class _Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file_encoding="utf-8")


class Config(_Settings):
    # Debug
    DEBUG: bool = Field(..., description="Debug mode")

    # Backend
    BACKEND_TITLE: str = Field(..., description="Backend title")
    BACKEND_DESCRIPTION: str = Field(..., description="Backend description")
    BACKEND_PREFIX: str = Field(..., description="Backend prefix")

    BACKEND_HOST: str = Field(..., description="Backend host")
    BACKEND_PORT: int = Field(..., description="Backend port")
    BACKEND_RELOAD: bool = Field(..., description="Backend reload")

    # Postgres
    POSTGRES_USER: str = Field(..., description="Postgres user")
    POSTGRES_PASSWORD: str = Field(..., description="Postgres password")
    POSTGRES_SERVER: str = Field(..., description="Postgres server")
    POSTGRES_PORT: int = Field(..., description="Postgres port")
    POSTGRES_DB: str = Field(..., description="Postgres database")
    EXTERNAL_POSTGRES_PORT: Optional[int] = Field(None, description="Postgres external port")

    # JWT
    JWT_SECRET: str = Field(..., description="JWT secret")
    JWT_ALGORITHM: str = Field(..., description="JWT algorithm")
    JWT_EXPIRES_AT: int = Field(..., description="JWT expires at")

    DB_DSN: Optional[AsyncPostgresDsn] = Field(None, description="Postgres uri for docker contaibers", validate_default=True)

    @field_validator("DB_DSN", mode="before")
    def create_db_uri(cls, v: Optional[str], info: FieldValidationInfo) -> Any:
        if isinstance(v, str):
            return v
        return AsyncPostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=info.data['POSTGRES_USER'],
            password=info.data['POSTGRES_PASSWORD'],
            host=info.data['POSTGRES_SERVER'],
            port=info.data['POSTGRES_PORT'],
            path=f"{info.data['POSTGRES_DB'] or ''}",
        )


@lru_cache()
def get_config(env_file: str = ".env") -> Config:
    return Config(_env_file=find_dotenv(env_file))
