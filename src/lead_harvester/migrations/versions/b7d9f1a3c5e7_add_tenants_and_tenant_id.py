"""Add tenants and tenant_id on canonical_institutions/branches/contact_points/service_credentials

Revision ID: b7d9f1a3c5e7
Revises: a5c7e9b1d3f5
Create Date: 2026-08-06 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "b7d9f1a3c5e7"
down_revision: str | Sequence[str] | None = "a5c7e9b1d3f5"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

# Matches models/tenancy.py::DEFAULT_TENANT_ID exactly -- every currently
# single-tenant row (and every ORM-level tenant_id default) resolves to
# this fixed identity.
_DEFAULT_TENANT_ID = "00000000-0000-0000-0000-000000000001"

_tenant_status = sa.Enum("ACTIVE", "SUSPENDED", name="tenantstatus")


def upgrade() -> None:
    """
    docs/ROADMAP.md Module 03 / delivery sequence Slice 1.1: the tenant
    boundary for the core resolved-entity tables. Nullable-add ->
    backfill -> not-null on every existing table, per this repo's own
    migration convention (AGENTS.md / docs/CODE_REVIEW_LESSONS.md pattern
    13) -- none of these four tables can be assumed empty.
    """
    # No standalone _tenant_status.create() here -- see
    # a5c7e9b1d3f5_add_service_credentials.py's identical comment for why:
    # op.create_table() below creates the "tenantstatus" enum type itself,
    # and creating it twice fails the second CREATE TYPE.
    op.create_table(
        "tenants",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("slug", sa.String(length=100), nullable=False),
        sa.Column("status", _tenant_status, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
        sa.UniqueConstraint("slug"),
    )
    op.create_index(op.f("ix_tenants_slug"), "tenants", ["slug"])

    tenants = sa.table(
        "tenants",
        sa.column("id", postgresql.UUID),
        sa.column("name", sa.String),
        sa.column("slug", sa.String),
        sa.column("status", _tenant_status),
        sa.column("created_at", sa.DateTime),
    )
    op.execute(
        tenants.insert().values(
            id=_DEFAULT_TENANT_ID,
            name="Default Tenant",
            slug="default",
            status="ACTIVE",
            created_at=sa.func.now(),
        )
    )

    for table_name in (
        "canonical_institutions",
        "branches",
        "contact_points",
        "service_credentials",
    ):
        op.add_column(
            table_name,
            sa.Column("tenant_id", postgresql.UUID(as_uuid=True), nullable=True),
        )
        op.execute(
            f"UPDATE {table_name} SET tenant_id = '{_DEFAULT_TENANT_ID}' WHERE tenant_id IS NULL"
        )
        op.alter_column(
            table_name, "tenant_id", existing_type=postgresql.UUID(as_uuid=True), nullable=False
        )
        op.create_foreign_key(
            f"fk_{table_name}_tenant_id", table_name, "tenants", ["tenant_id"], ["id"]
        )
        op.create_index(f"ix_{table_name}_tenant_id", table_name, ["tenant_id"])


def downgrade() -> None:
    for table_name in (
        "canonical_institutions",
        "branches",
        "contact_points",
        "service_credentials",
    ):
        op.drop_index(f"ix_{table_name}_tenant_id", table_name=table_name)
        op.drop_constraint(f"fk_{table_name}_tenant_id", table_name, type_="foreignkey")
        op.drop_column(table_name, "tenant_id")

    op.drop_index(op.f("ix_tenants_slug"), table_name="tenants")
    op.drop_table("tenants")
    _tenant_status.drop(op.get_bind(), checkfirst=True)
