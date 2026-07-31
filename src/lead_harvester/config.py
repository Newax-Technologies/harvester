from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

MIN_LEAD_SYNC_WEBHOOK_SECRET_LENGTH = 32


class Settings(BaseSettings):
    database_url: str = (
        "postgresql+asyncpg://postgres:development-only@localhost:5432/opportunity_engine"
    )
    test_database_url: str | None = (
        "postgresql+asyncpg://opportunity_test:TEST_PASSWORD@127.0.0.1:5432/lead_harvester_test"
    )
    google_places_api_key: str = ""
    yandex_maps_api_key: str = ""
    brave_search_api_key: str = ""
    # Apple MapKit Server API: a developer JWT is signed locally from these
    # three (team_id/key_id identify the signing key registered in App
    # Store Connect; private_key is the .p8 file's PEM contents) and
    # exchanged for a short-lived access token -- see sources/apple_maps.py.
    apple_maps_team_id: str = ""
    apple_maps_key_id: str = ""
    apple_maps_private_key: str = ""
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

    # Lead sync webhook (harvester -> core-newax)
    lead_sync_enabled: bool = False
    lead_sync_webhook_url: str = ""
    lead_sync_webhook_secret: str = ""
    lead_sync_webhook_timeout_seconds: float = 5.0
    lead_sync_default_country_code: str = "PK"

    # Ranking and Daily Selection (allocation/)
    daily_selection_default_limit: int = 25
    daily_selection_reservation_ttl_hours: float = 24.0
    daily_selection_min_score: int = 0

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @model_validator(mode="after")
    def _require_strong_webhook_secret_when_enabled(self) -> "Settings":
        if (
            self.lead_sync_enabled
            and len(self.lead_sync_webhook_secret) < MIN_LEAD_SYNC_WEBHOOK_SECRET_LENGTH
        ):
            raise ValueError(
                "LEAD_SYNC_WEBHOOK_SECRET must be at least "
                f"{MIN_LEAD_SYNC_WEBHOOK_SECRET_LENGTH} characters when LEAD_SYNC_ENABLED is true "
                "-- a short or empty secret signs every event with effectively no authenticity, "
                "and a correctly configured receiver will reject every delivery."
            )
        return self

    @model_validator(mode="after")
    def _require_webhook_url_when_enabled(self) -> "Settings":
        if self.lead_sync_enabled and not self.lead_sync_webhook_url.strip():
            raise ValueError(
                "LEAD_SYNC_WEBHOOK_URL must be set when LEAD_SYNC_ENABLED is true -- "
                "otherwise emit_institution_upserted() silently no-ops on every call, and "
                "with no retry/outbox, every event is lost with no indication anything is wrong."
            )
        return self

    def load_job_config(self) -> None:
        if self.job_config_path:
            import yaml

            with open(self.job_config_path, "r") as f:
                self.job_config = yaml.safe_load(f)


def validate_test_database_url(test_url: str, production_url: str) -> None:
    if test_url == production_url:
        raise RuntimeError("TEST_DATABASE_URL must not match DATABASE_URL.")

    if "test" not in test_url.lower():
        raise RuntimeError("Test database name must contain 'test'.")


settings = Settings()
