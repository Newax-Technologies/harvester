"""Add vaulted_credentials

Revision ID: d1e3f5a7b9c1
Revises: c9e1a3b5d7f9
Create Date: 2026-08-06 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "d1e3f5a7b9c1"
down_revision: str | Sequence[str] | None = "c9e1a3b5d7f9"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """
    Encrypted, versioned credential storage (docs/ROADMAP.md Module 09 /
    delivery sequence Slice 2.1). A row is never updated in place -- see
    models/vault.py's module docstring.
    """
    op.create_table(
        "vaulted_credentials",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("fingerprint", sa.String(length=64), nullable=False),
        sa.Column("ciphertext", sa.Text(), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_by", sa.String(length=255), nullable=False),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_vaulted_credentials_tenant_id"), "vaulted_credentials", ["tenant_id"])
    op.create_index(op.f("ix_vaulted_credentials_name"), "vaulted_credentials", ["name"])
    # Partial unique index: exactly one is_active=True row per
    # (tenant_id, name) -- matches tenant_config_overrides' identical
    # uq_tenant_config_one_active_version pattern.
    op.create_index(
        "uq_vaulted_credentials_one_active_version",
        "vaulted_credentials",
        ["tenant_id", "name"],
        unique=True,
        postgresql_where=sa.text("is_active = true"),
    )


def downgrade() -> None:
    op.drop_index("uq_vaulted_credentials_one_active_version", table_name="vaulted_credentials")
    op.drop_index(op.f("ix_vaulted_credentials_name"), table_name="vaulted_credentials")
    op.drop_index(op.f("ix_vaulted_credentials_tenant_id"), table_name="vaulted_credentials")
    op.drop_table("vaulted_credentials")
