"""Add last_recompute_attempted_at to lead_profiles

Revision ID: 99bebd9953d7
Revises: f4b6d8e0a2c4
Create Date: 2026-08-01 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "99bebd9953d7"
down_revision: str | Sequence[str] | None = "f4b6d8e0a2c4"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """
    Separate remediation-attempt cursor for
    services/lead_profile_service.py::recompute_all_lead_profiles --
    bumped on a failed refresh instead of computed_at, so a persistently
    failing profile's remediation cursor still advances without corrupting
    computed_at (the API-exposed freshness/trust signal) into claiming a
    still-untrusted profile was just freshly computed. Nullable, no
    backfill: NULL means "never had a failed recompute attempt", which is
    true for every pre-existing row.
    """
    op.add_column(
        "lead_profiles",
        sa.Column("last_recompute_attempted_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("lead_profiles", "last_recompute_attempted_at")
