import pytest

from lead_harvester.config import Settings

_VALID_WEBHOOK_URL = "https://core-newax.test/api/integrations/lead-harvester/webhook"


def test_rejects_short_webhook_secret_when_sync_enabled():
    with pytest.raises(ValueError, match="LEAD_SYNC_WEBHOOK_SECRET"):
        Settings(
            lead_sync_enabled=True,
            lead_sync_webhook_secret="too-short",
            lead_sync_webhook_url=_VALID_WEBHOOK_URL,
        )


def test_rejects_empty_webhook_secret_when_sync_enabled():
    with pytest.raises(ValueError, match="LEAD_SYNC_WEBHOOK_SECRET"):
        Settings(
            lead_sync_enabled=True,
            lead_sync_webhook_secret="",
            lead_sync_webhook_url=_VALID_WEBHOOK_URL,
        )


def test_accepts_strong_webhook_secret_when_sync_enabled():
    settings = Settings(
        lead_sync_enabled=True,
        lead_sync_webhook_secret="a-secret-with-more-than-32-characters",
        lead_sync_webhook_url=_VALID_WEBHOOK_URL,
    )
    assert settings.lead_sync_enabled is True


def test_allows_short_webhook_secret_when_sync_disabled():
    settings = Settings(lead_sync_enabled=False, lead_sync_webhook_secret="")
    assert settings.lead_sync_enabled is False


def test_rejects_empty_webhook_url_when_sync_enabled():
    with pytest.raises(ValueError, match="LEAD_SYNC_WEBHOOK_URL"):
        Settings(
            lead_sync_enabled=True,
            lead_sync_webhook_secret="a-secret-with-more-than-32-characters",
            lead_sync_webhook_url="",
        )


def test_allows_empty_webhook_url_when_sync_disabled():
    settings = Settings(lead_sync_enabled=False, lead_sync_webhook_url="")
    assert settings.lead_sync_enabled is False


def test_rejects_restricted_sources_enabled_in_production():
    with pytest.raises(ValueError, match="RESTRICTED_SOURCES_ENABLED"):
        Settings(restricted_sources_enabled=True, app_env="production")


def test_allows_restricted_sources_enabled_in_development_or_test():
    assert Settings(
        restricted_sources_enabled=True, app_env="development"
    ).restricted_sources_enabled
    assert Settings(restricted_sources_enabled=True, app_env="test").restricted_sources_enabled


def test_restricted_sources_disabled_by_default():
    settings = Settings()
    assert settings.restricted_sources_enabled is False


def test_allows_restricted_sources_disabled_in_production():
    settings = Settings(restricted_sources_enabled=False, app_env="production")
    assert settings.app_env == "production"


def test_rejects_dev_auth_enabled_in_production():
    with pytest.raises(ValueError, match="DEV_AUTH_ENABLED"):
        Settings(dev_auth_enabled=True, app_env="production")


def test_allows_dev_auth_enabled_in_development_or_test():
    assert Settings(dev_auth_enabled=True, app_env="development").dev_auth_enabled
    assert Settings(dev_auth_enabled=True, app_env="test").dev_auth_enabled


def test_dev_auth_disabled_by_default():
    settings = Settings()
    assert settings.dev_auth_enabled is False


@pytest.mark.parametrize("spelling", ["Production", "PRODUCTION", " production", "production "])
def test_rejects_restricted_sources_enabled_regardless_of_app_env_spelling(spelling):
    with pytest.raises(ValueError, match="RESTRICTED_SOURCES_ENABLED"):
        Settings(restricted_sources_enabled=True, app_env=spelling)


@pytest.mark.parametrize("spelling", ["Production", "PRODUCTION", " production", "production "])
def test_rejects_dev_auth_enabled_regardless_of_app_env_spelling(spelling):
    with pytest.raises(ValueError, match="DEV_AUTH_ENABLED"):
        Settings(dev_auth_enabled=True, app_env=spelling)


@pytest.mark.parametrize("non_dev_env", ["staging", "qa", "preview", "uat", ""])
def test_rejects_restricted_sources_enabled_in_any_non_dev_environment(non_dev_env):
    # Not just "production" -- staging/QA/preview/etc. are real, reachable
    # deployments too, and none of them is the literal string "production".
    with pytest.raises(ValueError, match="RESTRICTED_SOURCES_ENABLED"):
        Settings(restricted_sources_enabled=True, app_env=non_dev_env)


@pytest.mark.parametrize("non_dev_env", ["staging", "qa", "preview", "uat", ""])
def test_rejects_dev_auth_enabled_in_any_non_dev_environment(non_dev_env):
    with pytest.raises(ValueError, match="DEV_AUTH_ENABLED"):
        Settings(dev_auth_enabled=True, app_env=non_dev_env)


def test_app_env_is_normalized_to_lowercase_and_stripped():
    settings = Settings(app_env=" Production ")
    assert settings.app_env == "production"
