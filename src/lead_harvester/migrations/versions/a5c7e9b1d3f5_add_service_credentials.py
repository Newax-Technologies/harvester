"""Add service_credentials

Revision ID: a5c7e9b1d3f5
Revises: f4b6d8e0a2c4
Create Date: 2026-08-06 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "a5c7e9b1d3f5"
down_revision: str | Sequence[str] | None = "f4b6d8e0a2c4"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_service_role = sa.Enum("ADMIN", "REVIEWER", "VIEWER", name="servicerole")


def upgrade() -> None:
    """
    Real, revocable, expirable, hashed bearer credentials -- replaces the
    hardcoded "secret-admin-token"/"secret-reviewer-token" literals and the
    silent unrecognized-token-becomes-viewer fallback previously in
    api/dependencies.py::get_current_user.
    """
    # No standalone _service_role.create() here -- op.create_table() below
    # creates the "servicerole" enum type itself as part of creating this
    # brand-new table's "role" column; calling .create() first and then
    # creating the table would issue CREATE TYPE twice and fail the
    # second time with DuplicateObjectError, since create_table's own
    # enum-creation dispatch does not pass checkfirst=True.
    op.create_table(
        "service_credentials",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("role", _service_role, nullable=False),
        sa.Column("token_hash", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_used_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
        sa.UniqueConstraint("token_hash"),
    )
    op.create_index(
        op.f("ix_service_credentials_token_hash"), "service_credentials", ["token_hash"]
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_service_credentials_token_hash"), table_name="service_credentials")
    op.drop_table("service_credentials")
    _service_role.drop(op.get_bind(), checkfirst=True)
