"""
Reads and writes TenantConfigOverride rows against the config_registry.py
whitelist -- see that module's and models/tenant_config.py's docstrings.
"""

from __future__ import annotations

import uuid
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.config_registry import get_definition, validate_value
from lead_harvester.models.tenancy import Tenant
from lead_harvester.models.tenant_config import TenantConfigOverride
from lead_harvester.services.auth_service import TenantNotFoundError


async def get_tenant_config(session: AsyncSession, tenant_id: uuid.UUID, key: str) -> Any:
    """
    Returns the tenant's active override for `key`, or the registry
    default if none exists. Raises UnknownConfigKeyError for a key not
    in CONFIG_REGISTRY (via get_definition), or TenantNotFoundError if
    tenant_id matches no Tenant row -- without this, a typo'd or stale
    --tenant-id would silently print the registry default and exit 0, as
    though that tenant existed and simply had no override.
    """
    definition = get_definition(key)

    if await session.get(Tenant, tenant_id) is None:
        raise TenantNotFoundError(f"No tenant found with id {tenant_id}.")

    override = (
        await session.scalars(
            select(TenantConfigOverride).where(
                TenantConfigOverride.tenant_id == tenant_id,
                TenantConfigOverride.key == key,
                TenantConfigOverride.is_active.is_(True),
            )
        )
    ).first()
    return override.value["v"] if override is not None else definition.default


async def set_tenant_config(
    session: AsyncSession,
    tenant_id: uuid.UUID,
    key: str,
    value: Any,
    *,
    created_by: str,
) -> TenantConfigOverride:
    """
    Inserts a new version and deactivates the prior active version (if
    any) in the same flush -- never updates a row's value in place, so
    get_tenant_config_history() always has the full sequence. Raises
    UnknownConfigKeyError for a key not in CONFIG_REGISTRY,
    ConfigValueTypeError if `value` doesn't match that key's declared type,
    or TenantNotFoundError if tenant_id matches no row (a clean error
    instead of the FK's IntegrityError -- same reasoning as
    auth_service.issue_service_credential).
    """
    validate_value(key, value)

    if await session.get(Tenant, tenant_id) is None:
        raise TenantNotFoundError(f"No tenant found with id {tenant_id}.")

    # Transaction-scoped advisory lock on (tenant_id, key), held until this
    # transaction commits or rolls back. Needed even for the never-set-
    # before case below, where there is no row yet for a SELECT ... FOR
    # UPDATE to lock: without this, two concurrent callers can both read
    # "no active version", both compute next_version=1, and race on the
    # partial unique index (uq_tenant_config_one_active_version) -- one
    # succeeds, the other gets a raw IntegrityError instead of simply
    # waiting its turn and versioning on top of the winner.
    await session.execute(
        select(func.pg_advisory_xact_lock(func.hashtext(str(tenant_id)), func.hashtext(key)))
    )

    previous_active = (
        await session.scalars(
            select(TenantConfigOverride).where(
                TenantConfigOverride.tenant_id == tenant_id,
                TenantConfigOverride.key == key,
                TenantConfigOverride.is_active.is_(True),
            )
        )
    ).first()

    next_version = 1
    if previous_active is not None:
        previous_active.is_active = False
        next_version = previous_active.version + 1
    else:
        # A key can have prior (already-inactive) versions with no
        # currently-active row -- fall through to the highest version
        # ever recorded rather than restarting at 1 and colliding.
        highest = await session.scalar(
            select(TenantConfigOverride.version)
            .where(TenantConfigOverride.tenant_id == tenant_id, TenantConfigOverride.key == key)
            .order_by(TenantConfigOverride.version.desc())
            .limit(1)
        )
        if highest is not None:
            next_version = highest + 1

    # value is wrapped in {"v": ...} rather than stored bare -- JSONB
    # accepts any JSON value at the top level (including a raw scalar
    # `false` or `5`), but a bare column is awkward to query/index into
    # consistently across bool/int/string/list types; a stable object
    # shape keeps every key's storage uniform.
    override = TenantConfigOverride(
        tenant_id=tenant_id,
        key=key,
        value={"v": value},
        version=next_version,
        is_active=True,
        created_by=created_by,
    )
    session.add(override)
    await session.flush()
    return override


async def get_tenant_config_history(
    session: AsyncSession, tenant_id: uuid.UUID, key: str
) -> list[TenantConfigOverride]:
    """
    Every version ever recorded for this (tenant, key), oldest first.
    Raises UnknownConfigKeyError for an undeclared key, or
    TenantNotFoundError for a tenant_id that matches no Tenant row (see
    get_tenant_config's docstring for why this is checked explicitly
    rather than just returning an empty list).
    """
    get_definition(key)  # raises UnknownConfigKeyError for an undeclared key

    if await session.get(Tenant, tenant_id) is None:
        raise TenantNotFoundError(f"No tenant found with id {tenant_id}.")

    return list(
        await session.scalars(
            select(TenantConfigOverride)
            .where(TenantConfigOverride.tenant_id == tenant_id, TenantConfigOverride.key == key)
            .order_by(TenantConfigOverride.version.asc())
        )
    )
