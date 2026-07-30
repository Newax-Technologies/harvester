"""Add lead_synced_at to canonical_institutions

Revision ID: d5e7f9a1b3c5
Revises: c4d6e8f0a1b3
Create Date: 2026-07-30 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d5e7f9a1b3c5"
down_revision: str | Sequence[str] | None = "c4d6e8f0a1b3"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """
    Tracks whether integrations/lead_sync_emitter.py has ever attempted to
    sync this institution to core-newax -- gates whether a later resolution
    update (automated attach, or a reviewer decision) bothers re-emitting a
    sync event. Nullable, no backfill: every pre-existing institution
    predates this column and has never actually been synced (the emitter
    only exists as of this same PR), so NULL ("never synced") is the
    correct value for all of them.
    """
    op.add_column(
        "canonical_institutions",
        sa.Column("lead_synced_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("canonical_institutions", "lead_synced_at")
