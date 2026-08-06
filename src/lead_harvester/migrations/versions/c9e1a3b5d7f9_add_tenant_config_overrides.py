"""Add tenant_config_overrides

Revision ID: c9e1a3b5d7f9
Revises: b7d9f1a3c5e7
Create Date: 2026-08-06 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "c9e1a3b5d7f9"
down_revision: str | Sequence[str] | None = "b7d9f1a3c5e7"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """
    Versioned per-tenant configuration overrides (docs/ROADMAP.md Module 07 /
    delivery sequence Slice 1.4). A row is never updated in place -- see
    models/tenant_config.py's module docstring.
    """
    op.create_table(
        "tenant_config_overrides",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("key", sa.String(length=255), nullable=False),
        sa.Column("value", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_by", sa.String(length=255), nullable=False),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_tenant_config_overrides_tenant_id"), "tenant_config_overrides", ["tenant_id"]
    )
    op.create_index(op.f("ix_tenant_config_overrides_key"), "tenant_config_overrides", ["key"])
    # Partial unique index: exactly one is_active=True row per
    # (tenant_id, key) -- older versions (is_active=False) are exempt, so
    # history isn't capped at one row. Matches
    # a5c7e9b1d3f5_add_service_credentials.py's active-name index pattern.
    op.create_index(
        "uq_tenant_config_one_active_version",
        "tenant_config_overrides",
        ["tenant_id", "key"],
        unique=True,
        postgresql_where=sa.text("is_active = true"),
    )


def downgrade() -> None:
    op.drop_index("uq_tenant_config_one_active_version", table_name="tenant_config_overrides")
    op.drop_index(op.f("ix_tenant_config_overrides_key"), table_name="tenant_config_overrides")
    op.drop_index(
        op.f("ix_tenant_config_overrides_tenant_id"), table_name="tenant_config_overrides"
    )
    op.drop_table("tenant_config_overrides")
