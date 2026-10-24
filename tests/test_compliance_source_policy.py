import pytest

from lead_harvester.compliance.channel_eligibility import is_channel_eligible
from lead_harvester.compliance.source_policy import (
    SOURCE_POLICIES,
    AuthorizationBasis,
    RestrictedSourceDisabledError,
    contested_sources,
    ensure_source_enabled,
    get_source_policy,
)
from lead_harvester.models.compliance import SuppressionEntry, SuppressionReason
from lead_harvester.models.source import SourceType


def test_every_source_type_has_a_declared_policy():
    for source_type in SourceType:
        assert source_type in SOURCE_POLICIES


def test_get_source_policy_returns_the_registered_entry():
    policy = get_source_policy(SourceType.GOOGLE_PLACES)
    assert policy.authorization_basis == AuthorizationBasis.LICENSED_API


def test_linkedin_is_declared_as_account_automation_not_hidden_or_blessed():
    policy = get_source_policy(SourceType.LINKEDIN)
    assert policy.authorization_basis == AuthorizationBasis.ACCOUNT_AUTOMATION
    assert "CONTESTED" in policy.notes


def test_contested_sources_flags_linkedin():
    assert SourceType.LINKEDIN in contested_sources()


def test_contested_sources_does_not_flag_licensed_or_manual_sources():
    contested = contested_sources()
    assert SourceType.GOOGLE_PLACES not in contested
    assert SourceType.MANUAL not in contested
    assert SourceType.AUTHORIZED_IMPORT not in contested


def test_yandex_and_apple_maps_are_declared_licensed_api():
    assert (
        get_source_policy(SourceType.YANDEX).authorization_basis == AuthorizationBasis.LICENSED_API
    )
    assert (
        get_source_policy(SourceType.APPLE_MAPS).authorization_basis
        == AuthorizationBasis.LICENSED_API
    )


def test_telegram_is_declared_public_web_crawl_not_account_automation():
    policy = get_source_policy(SourceType.TELEGRAM)
    assert policy.authorization_basis == AuthorizationBasis.PUBLIC_WEB_CRAWL


def test_none_of_the_new_connectors_are_still_not_implemented():
    for source_type in (SourceType.TELEGRAM, SourceType.YANDEX, SourceType.APPLE_MAPS):
        assert (
            get_source_policy(source_type).authorization_basis != AuthorizationBasis.NOT_IMPLEMENTED
        )


def test_channel_eligible_when_no_suppression_exists():
    result = is_channel_eligible("email", None)
    assert result.eligible is True


def test_channel_ineligible_under_a_blanket_suppression():
    suppression = SuppressionEntry(
        normalized_contact_value="a@b.com", channel=None, reason=SuppressionReason.OPT_OUT
    )
    result = is_channel_eligible("email", suppression)
    assert result.eligible is False
    result_other_channel = is_channel_eligible("linkedin", suppression)
    assert result_other_channel.eligible is False


def test_channel_ineligible_only_for_the_matching_specific_channel():
    suppression = SuppressionEntry(
        normalized_contact_value="a@b.com", channel="email", reason=SuppressionReason.BOUNCED
    )
    assert is_channel_eligible("email", suppression).eligible is False
    assert is_channel_eligible("linkedin", suppression).eligible is True


def test_ensure_source_enabled_blocks_linkedin_when_restricted_sources_disabled():
    with pytest.raises(RestrictedSourceDisabledError, match="linkedin"):
        ensure_source_enabled(SourceType.LINKEDIN, restricted_sources_enabled=False)


def test_ensure_source_enabled_allows_linkedin_when_restricted_sources_enabled():
    ensure_source_enabled(SourceType.LINKEDIN, restricted_sources_enabled=True)


def test_ensure_source_enabled_never_blocks_non_account_automation_sources():
    for source_type in SourceType:
        if source_type == SourceType.LINKEDIN:
            continue
        ensure_source_enabled(source_type, restricted_sources_enabled=False)
