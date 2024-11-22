import tomllib
from pathlib import Path
from typing import Optional

from pydantic import computed_field, Field, AnyUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PGHOST: str
    PGDATABASE: str
    PGUSER: str
    PGPASSWORD: Optional[str] = Field(default="")
    PGPORT: Optional[int] = Field(default=5432)

    NAME: str
    DESCRIPTION: str
    VERSION: str
    BASE_DIR: Path
    DATA_DIR: Path

    REDIS_URL: AnyUrl

    AUTH_USERNAME: str
    AUTH_PASSWORD: str

    SENTRY_DSN: Optional[str] = Field(default=None)
    SENTRY_ENVIRONMENT: Optional[str] = Field(default=None)

    CLICKHOUSE_DB: str
    CLICKHOUSE_USER: str
    CLICKHOUSE_PASSWORD: str
    CLICKHOUSE_HOST: str
    CLICKHOUSE_PORT: int = Field(default=8123)
    CLICKHOUSE_BATCH_SIZE: int = Field(default=500_000)

    DRAMATIQ_TIMEOUT: int = Field(default=1_200_000)

    def __init__(self, *args, **kwargs):
        base_dir = Path(__file__).resolve(strict=True).parent.parent.parent
        kwargs.setdefault("BASE_DIR", base_dir)

        with open(base_dir / "pyproject.toml", "rb") as f:
            pyproject = tomllib.load(f)
            kwargs.setdefault("NAME", pyproject["tool"]["poetry"]["name"])
            kwargs.setdefault("DESCRIPTION", pyproject["tool"]["poetry"]["description"])
            kwargs.setdefault("VERSION", pyproject["tool"]["poetry"]["version"])

        super().__init__(*args, **kwargs)

    @computed_field
    def database_url(self) -> str:
        if self.PGPASSWORD:
            return (
                f"postgresql+psycopg://{self.PGUSER}:{self.PGPASSWORD}@{self.PGHOST}:{self.PGPORT}/{self.PGDATABASE}"
            )
        else:
            return f"postgresql+psycopg://{self.PGUSER}@{self.PGHOST}:{self.PGPORT}/{self.PGDATABASE}"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
