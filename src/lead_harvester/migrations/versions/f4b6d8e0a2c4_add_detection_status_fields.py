"""Add detection status fields to lead_profiles

Revision ID: f4b6d8e0a2c4
Revises: 99bebd9953d7
Create Date: 2026-08-01 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "f4b6d8e0a2c4"
down_revision: str | Sequence[str] | None = "99bebd9953d7"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_detection_status = sa.Enum(
    "PRESENT",
    "ABSENT_CONFIRMED",
    "NOT_DETECTED",
    "NOT_CRAWLED",
    "CRAWL_FAILED",
    "UNKNOWN",
    name="detectionstatus",
)


def upgrade() -> None:
    """Persist evidence-backed website and LMS detection states."""
    _detection_status.create(op.get_bind(), checkfirst=True)
    op.add_column(
        "lead_profiles",
        sa.Column("website_detection_status", _detection_status, nullable=True),
    )
    op.add_column(
        "lead_profiles",
        sa.Column("lms_detection_status", _detection_status, nullable=True),
    )

    lead_profiles = sa.table(
        "lead_profiles",
        sa.column("website_detection_status", _detection_status),
        sa.column("lms_detection_status", _detection_status),
    )
    op.execute(
        lead_profiles.update().values(
            website_detection_status="UNKNOWN", lms_detection_status="UNKNOWN"
        )
    )

    op.alter_column(
        "lead_profiles",
        "website_detection_status",
        existing_type=_detection_status,
        nullable=False,
    )
    op.alter_column(
        "lead_profiles", "lms_detection_status", existing_type=_detection_status, nullable=False
    )


def downgrade() -> None:
    op.drop_column("lead_profiles", "lms_detection_status")
    op.drop_column("lead_profiles", "website_detection_status")
    _detection_status.drop(op.get_bind(), checkfirst=True)
