"""Add review_outcome to resolution_candidates

Revision ID: a4b6c8d0e2f4
Revises: f1a2b3c4d5e6
Create Date: 2026-07-29 12:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a4b6c8d0e2f4"
down_revision: str | Sequence[str] | None = "f1a2b3c4d5e6"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_review_outcome = sa.Enum("MERGED", "BRANCHED", "SEPARATED", name="reviewoutcome")


def upgrade() -> None:
    """Upgrade schema."""
    # A bare ADD COLUMN (unlike CREATE TABLE) does not implicitly create the
    # backing Postgres enum type, so it must be created explicitly first.
    _review_outcome.create(op.get_bind(), checkfirst=True)
    op.add_column(
        "resolution_candidates",
        sa.Column("review_outcome", _review_outcome, nullable=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("resolution_candidates", "review_outcome")
    _review_outcome.drop(op.get_bind(), checkfirst=True)
