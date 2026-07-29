import pytest

from lead_harvester.config import Settings


def test_rejects_short_webhook_secret_when_sync_enabled():
    with pytest.raises(ValueError, match="LEAD_SYNC_WEBHOOK_SECRET"):
        Settings(lead_sync_enabled=True, lead_sync_webhook_secret="too-short")


def test_rejects_empty_webhook_secret_when_sync_enabled():
    with pytest.raises(ValueError, match="LEAD_SYNC_WEBHOOK_SECRET"):
        Settings(lead_sync_enabled=True, lead_sync_webhook_secret="")


def test_accepts_strong_webhook_secret_when_sync_enabled():
    settings = Settings(
        lead_sync_enabled=True,
        lead_sync_webhook_secret="a-secret-with-more-than-32-characters",
    )
    assert settings.lead_sync_enabled is True


def test_allows_short_webhook_secret_when_sync_disabled():
    settings = Settings(lead_sync_enabled=False, lead_sync_webhook_secret="")
    assert settings.lead_sync_enabled is False
