from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:development-only@localhost:5432/opportunity_engine"
    test_database_url: Optional[str] = "postgresql+asyncpg://opportunity_test:TEST_PASSWORD@127.0.0.1:5432/lead_harvester_test"
    google_places_api_key: str = ""
    job_config_path: str = ""
    app_env: str = "development"
    allow_demo_seed: bool = False
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

def validate_test_database_url(test_url: str, production_url: str) -> None:
    if test_url == production_url:
        raise RuntimeError(
            "TEST_DATABASE_URL must not match DATABASE_URL."
        )

    if "test" not in test_url.lower():
        raise RuntimeError(
            "Test database name must contain 'test'."
        )

settings = Settings()
