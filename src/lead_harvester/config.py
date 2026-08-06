from dotenv import load_dotenv
from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Local development keeps ordinary configuration in .env and credentials in
# .env.secrets. Load the secrets file first so it wins over duplicate values
# in .env, while real process/deployment environment variables still keep the
# highest priority because override=False never replaces an existing value.
load_dotenv(".env.secrets", override=False)
load_dotenv(".env", override=False)

MIN_LEAD_SYNC_WEBHOOK_SECRET_LENGTH = 32

# Allowlist, not a denylist -- DEV_AUTH_ENABLED and RESTRICTED_SOURCES_ENABLED
# must only ever be true in an environment explicitly declared safe for
# them. Blocking only the literal "production" string (the original
# version of these guards) left every other real deployment -- staging,
# QA, preview, UAT -- able to set either flag and get unauthenticated
# admin access or run restricted LinkedIn automation, since none of
# those spellings are "production".
_ENVIRONMENTS_ALLOWING_DEV_GUARDS = frozenset({"development", "test"})


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

    # docs/ROADMAP.md Module 28 (Professional-Network Discovery) is
    # Restricted: account automation against real LinkedIn accounts
    # (stealth fingerprinting, CAPTCHA solving, human-emulated timing --
    # sources/linkedin_stealth.py, sources/account_farm.py,
    # outreach/automator.py) stays disabled until access, legal, security,
    # compliance, and operational approval are recorded (see
    # compliance/source_policy.py's LINKEDIN entry). False by default, and
    # the validator below refuses to let it be true in production even if
    # the environment variable is set.
    restricted_sources_enabled: bool = False

    # api/dependencies.py::get_current_user's local-development bypass --
    # replaces the previous unconditional os.getenv("DEV_AUTH_ENABLED")
    # read. False by default; the validator below refuses to let it be
    # true in production even if the environment variable is set, so a
    # deployment misconfiguration can't grant every request admin access.
    dev_auth_enabled: bool = False
    dev_auth_user: str = "local-admin"

    # services/credential_vault_service.py's at-rest encryption key for
    # vaulted connector/source credentials -- a Fernet key (32 url-safe
    # base64-encoded bytes). Unset by default; vault_crypto.py raises a
    # clear VaultNotConfiguredError the moment anything tries to
    # encrypt/decrypt without it, rather than this failing at import time
    # for deployments that never touch the vault.
    vault_encryption_key: str = ""

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

    # ICP matching (intelligence/icp_matching.py) -- an empty list means
    # "no preference stated for this criterion", not "matches nothing";
    # see icp_matching.py's own docstring for the full weighting.
    icp_target_institution_types: list[str] = []
    icp_min_branch_count: int = 0

    model_config = SettingsConfigDict(
        env_file=(".env", ".env.secrets"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @field_validator("app_env", mode="before")
    @classmethod
    def _normalize_app_env(cls, value: str) -> str:
        # "Production"/"PRODUCTION"/"prod "/etc. must not silently evade
        # the app_env == "production" guards below (RESTRICTED_SOURCES_ENABLED,
        # DEV_AUTH_ENABLED) -- normalize once here rather than trusting every
        # comparison site to defend itself (seed.py already had to add its
        # own .lower() for exactly this reason).
        return value.strip().lower() if isinstance(value, str) else value

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

    @model_validator(mode="after")
    def _forbid_restricted_sources_outside_allowed_environments(self) -> "Settings":
        if (
            self.restricted_sources_enabled
            and self.app_env not in _ENVIRONMENTS_ALLOWING_DEV_GUARDS
        ):
            raise ValueError(
                f"RESTRICTED_SOURCES_ENABLED must not be true when APP_ENV={self.app_env!r} -- "
                "docs/ROADMAP.md Module 28 keeps LinkedIn account automation Restricted "
                f"everywhere except {sorted(_ENVIRONMENTS_ALLOWING_DEV_GUARDS)}. A staging, QA, "
                "or preview deployment is not 'production' by name but is still a real, "
                "reachable environment this flag must not be true in."
            )
        return self

    @model_validator(mode="after")
    def _forbid_dev_auth_outside_allowed_environments(self) -> "Settings":
        if self.dev_auth_enabled and self.app_env not in _ENVIRONMENTS_ALLOWING_DEV_GUARDS:
            raise ValueError(
                f"DEV_AUTH_ENABLED must not be true when APP_ENV={self.app_env!r} -- it bypasses "
                "credential checks entirely and grants every request admin access. It may only "
                f"be set when APP_ENV is one of {sorted(_ENVIRONMENTS_ALLOWING_DEV_GUARDS)}, not "
                "merely 'not production' -- staging, QA, and preview deployments are real, "
                "reachable environments too."
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
