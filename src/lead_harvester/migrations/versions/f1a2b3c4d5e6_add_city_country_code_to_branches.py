"""Add city and country_code to branches

Revision ID: f1a2b3c4d5e6
Revises: b007b9280dac
Create Date: 2026-07-29 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f1a2b3c4d5e6"
down_revision: str | Sequence[str] | None = "b007b9280dac"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

# Existing rows (and the manual-lead form, historically) allow a blank city and
# store a free-text country name rather than an ISO-2 code, so these columns
# can't simply be added as NOT NULL -- add them nullable, backfill existing
# rows with an explicit placeholder, then enforce NOT NULL once every row is
# known to have a value.
_UNKNOWN_CITY = "Unknown"
_UNKNOWN_COUNTRY_CODE = "XX"


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("branches", sa.Column("city", sa.String(length=128), nullable=True))
    op.add_column("branches", sa.Column("country_code", sa.String(length=2), nullable=True))

    branches = sa.table(
        "branches",
        sa.column("city", sa.String),
        sa.column("country_code", sa.String),
    )
    op.execute(
        branches.update()
        .where(sa.or_(branches.c.city.is_(None), branches.c.city == ""))
        .values(city=_UNKNOWN_CITY)
    )
    op.execute(
        branches.update()
        .where(branches.c.country_code.is_(None))
        .values(country_code=_UNKNOWN_COUNTRY_CODE)
    )

    op.alter_column("branches", "city", existing_type=sa.String(length=128), nullable=False)
    op.alter_column("branches", "country_code", existing_type=sa.String(length=2), nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("branches", "country_code")
    op.drop_column("branches", "city")
