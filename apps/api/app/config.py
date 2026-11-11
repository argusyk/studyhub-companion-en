"""Settings from the environment (a local .env in apps/api or in the repository root)."""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=(".env", "../../.env"), extra="ignore")

    # For local development without Docker, a SQLite file is enough.
    database_url: str = "sqlite:///./studyhub_dev.sqlite3"
    department_tz: str = "Europe/Kyiv"


@lru_cache
def get_settings() -> Settings:
    return Settings()
