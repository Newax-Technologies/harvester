"""Add lead reservation model

Revision ID: f9c1a3e5b7d9
Revises: f3a5c7e9b1d3
Create Date: 2026-07-30 20:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f9c1a3e5b7d9"
down_revision: str | Sequence[str] | None = "f3a5c7e9b1d3"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "lead_reservations",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("institution_id", sa.UUID(), nullable=False),
        sa.Column(
            "status",
            sa.Enum("RESERVED", "CONSUMED", "EXPIRED", "RELEASED", name="reservationstatus"),
            nullable=False,
        ),
        sa.Column("score_at_reservation", sa.Integer(), nullable=False),
        sa.Column("batch_label", sa.String(length=64), nullable=False),
        sa.Column("reserved_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("consumed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("released_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["institution_id"],
            ["canonical_institutions.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_lead_reservations_institution_id"),
        "lead_reservations",
        ["institution_id"],
        unique=False,
    )

    # Defense in depth alongside the claim query's SKIP LOCKED: even if a
    # future caller ever creates a reservation outside
    # daily_selection_service.py's own locked claim path, the database
    # itself refuses a second 'reserved' row for an institution that
    # already has one -- a partial unique index (only 'reserved' rows
    # participate) rather than a plain unique constraint, since CONSUMED/
    # EXPIRED/RELEASED history rows for the same institution must be able
    # to accumulate over time.
    op.execute(
        "CREATE UNIQUE INDEX ix_lead_reservations_one_active_per_institution "
        "ON lead_reservations (institution_id) WHERE status = 'RESERVED'"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP INDEX IF EXISTS ix_lead_reservations_one_active_per_institution")
    op.drop_index(op.f("ix_lead_reservations_institution_id"), table_name="lead_reservations")
    op.drop_table("lead_reservations")
    op.execute("DROP TYPE IF EXISTS reservationstatus")
