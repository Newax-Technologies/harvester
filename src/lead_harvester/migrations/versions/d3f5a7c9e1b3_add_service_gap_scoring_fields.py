"""Add service gap scoring fields (module 20)

Revision ID: d3f5a7c9e1b3
Revises: c1e3a5b7d9f1
Create Date: 2026-08-01 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d3f5a7c9e1b3"
down_revision: str | Sequence[str] | None = "c1e3a5b7d9f1"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_website_quality_tier = sa.Enum(
    "NONE", "POOR", "ADEQUATE", "GOOD", "EXCEPTIONAL", name="websitequalitytier"
)


def upgrade() -> None:
    """Upgrade schema."""
    _website_quality_tier.create(op.get_bind(), checkfirst=True)
    op.add_column(
        "lead_profiles",
        sa.Column(
            "website_quality_tier", _website_quality_tier, nullable=False, server_default="NONE"
        ),
    )
    op.add_column(
        "lead_profiles",
        sa.Column("service_gap_score", sa.Float(), nullable=False, server_default="0"),
    )

    # New SignalType value -- see models/signal.py.
    op.execute("ALTER TYPE signaltype ADD VALUE IF NOT EXISTS 'TECHNOLOGY_PRESENT'")


def downgrade() -> None:
    """Downgrade schema."""
    # Postgres has no DROP VALUE for enums -- the TECHNOLOGY_PRESENT label
    # is left in place on downgrade, matching how this repo's other enum-
    # value-only migrations handle the same limitation.
    op.drop_column("lead_profiles", "service_gap_score")
    op.drop_column("lead_profiles", "website_quality_tier")
    _website_quality_tier.drop(op.get_bind(), checkfirst=True)
