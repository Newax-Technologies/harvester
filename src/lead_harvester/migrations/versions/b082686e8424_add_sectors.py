"""add sectors

Revision ID: b082686e8424
Revises: b5d7f9a1c3e5
Create Date: 2026-07-31 11:23:22.044876

"""

import uuid
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "b082686e8424"
down_revision: str | Sequence[str] | None = "b5d7f9a1c3e5"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

# See docs/ROADMAP.md module 16 -- a starting point, not a closed list.
# Adding a new sector later is a row insert (or a POST /api/v1/sectors
# call), not a migration.
_SEED_SECTORS: list[dict] = [
    {
        "code": "education",
        "display_name": "Education",
        "institution_types": ["school", "college", "university", "academy"],
    },
    {
        "code": "healthcare",
        "display_name": "Healthcare",
        "institution_types": ["clinic", "hospital", "pharmacy", "diagnostic_lab", "dental_clinic"],
    },
    {
        "code": "retail",
        "display_name": "Retail",
        "institution_types": ["retail_store", "supermarket", "boutique", "showroom"],
    },
    {
        "code": "legal",
        "display_name": "Legal",
        "institution_types": ["law_firm", "legal_services"],
    },
    {
        "code": "finance",
        "display_name": "Finance",
        "institution_types": ["bank", "insurance_agency", "accounting_firm", "financial_advisory"],
    },
    {
        "code": "transportation",
        "display_name": "Transportation",
        "institution_types": [
            "logistics_company",
            "courier_service",
            "freight_forwarder",
            "transport_company",
        ],
    },
    {
        "code": "real_estate",
        "display_name": "Real Estate",
        "institution_types": ["real_estate_agency", "property_developer"],
    },
    {
        "code": "hospitality",
        "display_name": "Hospitality",
        "institution_types": ["hotel", "restaurant", "event_venue"],
    },
]


def upgrade() -> None:
    """Upgrade schema."""
    sectors_table = op.create_table(
        "sectors",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("code", sa.String(length=50), nullable=False),
        sa.Column("display_name", sa.String(length=100), nullable=False),
        sa.Column("institution_types", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("icp_criteria", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("qualification_rules", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_sectors_code"), "sectors", ["code"], unique=True)

    op.bulk_insert(
        sectors_table,
        [
            {
                "id": uuid.uuid4(),
                "code": seed["code"],
                "display_name": seed["display_name"],
                "institution_types": seed["institution_types"],
                "icp_criteria": {},
                "qualification_rules": {},
            }
            for seed in _SEED_SECTORS
        ],
    )

    op.add_column("canonical_institutions", sa.Column("sector_id", sa.UUID(), nullable=True))
    op.create_index(
        op.f("ix_canonical_institutions_sector_id"),
        "canonical_institutions",
        ["sector_id"],
        unique=False,
    )
    op.create_foreign_key(
        "fk_canonical_institutions_sector_id_sectors",
        "canonical_institutions",
        "sectors",
        ["sector_id"],
        ["id"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "fk_canonical_institutions_sector_id_sectors",
        "canonical_institutions",
        type_="foreignkey",
    )
    op.drop_index(op.f("ix_canonical_institutions_sector_id"), table_name="canonical_institutions")
    op.drop_column("canonical_institutions", "sector_id")

    op.drop_index(op.f("ix_sectors_code"), table_name="sectors")
    op.drop_table("sectors")
