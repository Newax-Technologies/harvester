"""Add event outbox

Revision ID: c5e7a9b1d3f5
Revises: b2d4f6a8c0e2
Create Date: 2026-08-01 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "c5e7a9b1d3f5"
down_revision: str | Sequence[str] | None = "b2d4f6a8c0e2"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "event_outbox",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("institution_id", sa.UUID(), nullable=False),
        sa.Column("event_type", sa.String(length=100), nullable=False),
        sa.Column("payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column(
            "status",
            sa.Enum("PENDING", "DELIVERED", "FAILED", "DEAD_LETTER", name="outboxstatus"),
            nullable=False,
        ),
        sa.Column("attempt_count", sa.Integer(), nullable=False),
        sa.Column("next_attempt_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_error", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("delivered_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["institution_id"], ["canonical_institutions.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_event_outbox_institution_id"), "event_outbox", ["institution_id"], unique=False
    )
    op.create_index(
        op.f("ix_event_outbox_next_attempt_at"), "event_outbox", ["next_attempt_at"], unique=False
    )
    op.create_index(op.f("ix_event_outbox_status"), "event_outbox", ["status"], unique=False)
    # Claim queries filter on (status, next_attempt_at) together -- a
    # composite index matches that access pattern directly instead of
    # relying on the planner to intersect the two single-column indexes.
    op.create_index(
        "ix_event_outbox_status_next_attempt_at",
        "event_outbox",
        ["status", "next_attempt_at"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("ix_event_outbox_status_next_attempt_at", table_name="event_outbox")
    op.drop_index(op.f("ix_event_outbox_status"), table_name="event_outbox")
    op.drop_index(op.f("ix_event_outbox_next_attempt_at"), table_name="event_outbox")
    op.drop_index(op.f("ix_event_outbox_institution_id"), table_name="event_outbox")
    op.drop_table("event_outbox")
    op.execute("DROP TYPE IF EXISTS outboxstatus")
