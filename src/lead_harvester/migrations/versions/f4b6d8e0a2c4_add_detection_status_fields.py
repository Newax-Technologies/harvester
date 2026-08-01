"""Add detection status fields to lead_profiles

Revision ID: f4b6d8e0a2c4
Revises: e2a4c6f8b0d2
Create Date: 2026-08-01 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f4b6d8e0a2c4"
down_revision: str | Sequence[str] | None = "e2a4c6f8b0d2"
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
    """
    Correction (docs/ROADMAP.md module 20): service_gap_score's two
    products (website, LMS) previously only ever recorded "absent"
    (via WebsiteQualityTier.NONE / the plain presence-or-not of a
    TECHNOLOGY_PRESENT signal), collapsing "confirmed missing" and "we
    just don't know" into the same maximum-confidence bucket. These two
    columns store the actual DetectionStatus (models/profile.py) behind
    each half of the score -- see intelligence/detection_status.py and
    intelligence/service_gap.py's _DETECTION_GAP_WEIGHT.

    UNKNOWN default (not ABSENT_CONFIRMED, not PRESENT): correct for
    every pre-existing LeadProfile row, none of which has ever had this
    evidence computed -- see the recompute-lead-profiles CLI command
    (added alongside migration e2a4c6f8b0d2) for how to replace this
    default with a real, evidence-backed value.

    Staged nullable -> backfill -> not-null (AGENTS.md convention for any
    new required column on a table that may already have rows), not
    added NOT NULL directly.
    """
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
