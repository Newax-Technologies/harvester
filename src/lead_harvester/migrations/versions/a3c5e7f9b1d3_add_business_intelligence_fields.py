"""Add business intelligence fields to lead_profiles

Revision ID: a3c5e7f9b1d3
Revises: d7f9b1c3e5a7
Create Date: 2026-08-01 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a3c5e7f9b1d3"
down_revision: str | Sequence[str] | None = "d7f9b1c3e5a7"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_size_tier = sa.Enum("UNKNOWN", "SMALL", "MEDIUM", "LARGE", name="sizetier")


def upgrade() -> None:
    """Upgrade schema."""
    # A bare ADD COLUMN (unlike CREATE TABLE) does not implicitly create the
    # backing Postgres enum type, so it must be created explicitly first.
    _size_tier.create(op.get_bind(), checkfirst=True)
    op.add_column(
        "lead_profiles",
        sa.Column("size_tier", _size_tier, nullable=False, server_default="UNKNOWN"),
    )
    op.add_column(
        "lead_profiles",
        sa.Column("operational_maturity_score", sa.Integer(), nullable=False, server_default="0"),
    )
    op.add_column(
        "lead_profiles",
        sa.Column("icp_match_score", sa.Integer(), nullable=False, server_default="0"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("lead_profiles", "icp_match_score")
    op.drop_column("lead_profiles", "operational_maturity_score")
    op.drop_column("lead_profiles", "size_tier")
    _size_tier.drop(op.get_bind(), checkfirst=True)
