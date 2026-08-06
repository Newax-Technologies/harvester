import pytest

from lead_harvester.config_registry import (
    CONFIG_REGISTRY,
    ConfigValueType,
    ConfigValueTypeError,
    UnknownConfigKeyError,
    get_definition,
    validate_value,
)


def test_get_definition_returns_a_registered_key():
    definition = get_definition("feature.restricted_sources_enabled")
    assert definition.value_type == ConfigValueType.BOOL
    assert definition.default is False


def test_get_definition_rejects_an_unknown_key():
    with pytest.raises(UnknownConfigKeyError):
        get_definition("not.a.real.key")


def test_validate_value_accepts_matching_bool():
    validate_value("feature.restricted_sources_enabled", True)


def test_validate_value_rejects_int_for_bool_key():
    with pytest.raises(ConfigValueTypeError):
        validate_value("feature.restricted_sources_enabled", 1)


def test_validate_value_rejects_bool_for_int_key():
    with pytest.raises(ConfigValueTypeError):
        validate_value("limit.daily_selection_max_reservations", True)


def test_validate_value_accepts_matching_int():
    validate_value("limit.daily_selection_max_reservations", 10)


def test_validate_value_rejects_wrong_type_for_int_key():
    with pytest.raises(ConfigValueTypeError):
        validate_value("limit.daily_selection_max_reservations", "10")


def test_every_registered_default_passes_its_own_validation():
    # A registry entry whose own default fails its own type check would be
    # a self-inconsistent definition -- every default must be usable as
    # the value get_tenant_config() falls back to.
    for key in CONFIG_REGISTRY:
        validate_value(key, CONFIG_REGISTRY[key].default)
