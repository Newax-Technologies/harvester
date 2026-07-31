from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:development-only@localhost:5432/opportunity_engine"
    test_database_url: Optional[str] = "postgresql+asyncpg://opportunity_test:TEST_PASSWORD@127.0.0.1:5432/lead_harvester_test"
    google_places_api_key: str = ""
    brave_search_api_key: str = ""
    email_verification_api_url: str = ""
    email_verification_api_key: str = ""
    crm_api_url: str = ""
    crm_api_key: str = ""
    job_config_path: str = ""
    job_config: dict = {}
    app_env: str = "development"
    allow_demo_seed: bool = False
    
    # WebCrawler settings
    user_agent: str = "LeadBot/1.0"
    request_timeout_seconds: float = 10.0
    concurrency: int = 5
    delay_seconds: float = 1.0
    max_pages_per_domain: int = 50
    max_depth: int = 2
    max_response_bytes: int = 5 * 1024 * 1024
    keywords: list[str] = []
    intent_terms: list[str] = []

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    def load_job_config(self) -> None:
        if self.job_config_path:
            import yaml
            with open(self.job_config_path, 'r') as f:
                self.job_config = yaml.safe_load(f)

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
