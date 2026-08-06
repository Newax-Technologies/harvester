"""
Explicit tenant-configuration and entitlement catalog -- docs/ROADMAP.md
Modules 07 (Product Configuration and Environment Profiles) and 60
(Licensing and Feature Entitlements) / docs/delivery/
agency-intelligence-implementation-sequence.md Slice 1.4.

Mirrors authz.py's PERMISSIONS pattern: a config or entitlement key must
be declared here, with a type and a safe default, before
services/tenant_config_service.py will accept a tenant override for it.
This is a whitelist, not just documentation -- it is also how "no
plaintext secrets in configuration" is enforced. Module 09's credential
vault (not built yet) owns secrets; this registry has no key type for
one, and set_tenant_config() (services/tenant_config_service.py) refuses
any key not listed here, so a secret can't be smuggled in under an
unlisted name either.
"""

from __future__ import annotations

import enum
from dataclasses import dataclass
from typing import Any


class ConfigValueType(str, enum.Enum):
    BOOL = "bool"
    INT = "int"
    STRING = "string"
    STRING_LIST = "string_list"


@dataclass(frozen=True)
class ConfigKeyDefinition:
    value_type: ConfigValueType
    default: Any
    description: str


# Key -> definition. Dotted namespaces group related settings
# ("feature.", "entitlement.connectors.", "limit.") without implying any
# structure the store itself enforces -- each key is still a flat,
# independently versioned override.
CONFIG_REGISTRY: dict[str, ConfigKeyDefinition] = {
    "feature.restricted_sources_enabled": ConfigKeyDefinition(
        value_type=ConfigValueType.BOOL,
        default=False,
        description=(
            "Per-tenant override of the global RESTRICTED_SOURCES_ENABLED gate "
            "(compliance/source_policy.py). The global Settings flag stays the hard "
            "production ceiling -- see config.py's _forbid_restricted_sources_in_production -- "
            "this can only narrow it further for a specific tenant, never widen it."
        ),
    ),
    "entitlement.connectors.google_places": ConfigKeyDefinition(
        value_type=ConfigValueType.BOOL,
        default=True,
        description="May use the Google Places connector.",
    ),
    "entitlement.connectors.yandex_maps": ConfigKeyDefinition(
        value_type=ConfigValueType.BOOL,
        default=True,
        description="May use the Yandex Maps connector.",
    ),
    "entitlement.connectors.apple_maps": ConfigKeyDefinition(
        value_type=ConfigValueType.BOOL,
        default=True,
        description="May use the Apple Maps connector.",
    ),
    "entitlement.connectors.telegram": ConfigKeyDefinition(
        value_type=ConfigValueType.BOOL,
        default=True,
        description="May use the Telegram public-channel connector.",
    ),
    "limit.daily_selection_max_reservations": ConfigKeyDefinition(
        value_type=ConfigValueType.INT,
        default=25,
        description="Upper bound on select-daily-leads' --limit for this tenant.",
    ),
    "limit.export_max_rows": ConfigKeyDefinition(
        value_type=ConfigValueType.INT,
        default=5000,
        description="Upper bound on a single export job's row count.",
    ),
}


class UnknownConfigKeyError(ValueError):
    """Raised for any key not present in CONFIG_REGISTRY."""


class ConfigValueTypeError(ValueError):
    """Raised when a value doesn't match its key's declared ConfigValueType."""


def get_definition(key: str) -> ConfigKeyDefinition:
    try:
        return CONFIG_REGISTRY[key]
    except KeyError:
        raise UnknownConfigKeyError(
            f"{key!r} is not a declared configuration key -- see config_registry.CONFIG_REGISTRY. "
            "Add it there before it can be set for any tenant."
        ) from None


def validate_value(key: str, value: Any) -> None:
    definition = get_definition(key)
    value_type = definition.value_type

    # bool is a subclass of int in Python -- isinstance(value, int) alone
    # would accept True/False for an INT key, so bool is checked first
    # and INT explicitly excludes it.
    is_valid = (
        (value_type == ConfigValueType.BOOL and isinstance(value, bool))
        or (
            value_type == ConfigValueType.INT
            and isinstance(value, int)
            and not isinstance(value, bool)
        )
        or (value_type == ConfigValueType.STRING and isinstance(value, str))
        or (
            value_type == ConfigValueType.STRING_LIST
            and isinstance(value, list)
            and all(isinstance(item, str) for item in value)
        )
    )
    if not is_valid:
        raise ConfigValueTypeError(f"{key!r} expects a {value_type.value}, got {value!r}.")
