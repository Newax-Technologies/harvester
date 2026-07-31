"""Add raw_page_snapshots

Revision ID: b5d7f9a1c3e5
Revises: a3c5e7f9b1d3
Create Date: 2026-08-01 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b5d7f9a1c3e5"
down_revision: str | Sequence[str] | None = "a3c5e7f9b1d3"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "raw_page_snapshots",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("source_run_id", sa.UUID(), nullable=False),
        sa.Column("url", sa.String(length=2048), nullable=False),
        sa.Column("final_url", sa.String(length=2048), nullable=False),
        sa.Column("status_code", sa.Integer(), nullable=True),
        sa.Column("content_type", sa.String(length=255), nullable=False),
        sa.Column("html", sa.Text(), nullable=True),
        sa.Column("fetch_error", sa.String(length=255), nullable=False),
        sa.Column("fetched_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["source_run_id"], ["source_runs.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_raw_page_snapshots_source_run_id"),
        "raw_page_snapshots",
        ["source_run_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_raw_page_snapshots_fetched_at"), "raw_page_snapshots", ["fetched_at"], unique=False
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_raw_page_snapshots_fetched_at"), table_name="raw_page_snapshots")
    op.drop_index(op.f("ix_raw_page_snapshots_source_run_id"), table_name="raw_page_snapshots")
    op.drop_table("raw_page_snapshots")
