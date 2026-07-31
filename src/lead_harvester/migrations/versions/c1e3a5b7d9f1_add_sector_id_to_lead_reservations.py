"""add sector_id to lead_reservations

Revision ID: c1e3a5b7d9f1
Revises: b082686e8424
Create Date: 2026-07-31 16:15:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c1e3a5b7d9f1"
down_revision: str | Sequence[str] | None = "b082686e8424"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("lead_reservations", sa.Column("sector_id", sa.UUID(), nullable=True))
    op.create_index(
        op.f("ix_lead_reservations_sector_id"), "lead_reservations", ["sector_id"], unique=False
    )
    op.create_foreign_key(
        "fk_lead_reservations_sector_id_sectors",
        "lead_reservations",
        "sectors",
        ["sector_id"],
        ["id"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "fk_lead_reservations_sector_id_sectors", "lead_reservations", type_="foreignkey"
    )
    op.drop_index(op.f("ix_lead_reservations_sector_id"), table_name="lead_reservations")
    op.drop_column("lead_reservations", "sector_id")
