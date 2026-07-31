"""Add CRM sync records

Revision ID: a7c9d1e3f5b8
Revises: f1a2b3c4d5e6
Create Date: 2026-07-31 01:20:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a7c9d1e3f5b8'
down_revision: Union[str, Sequence[str], None] = 'f1a2b3c4d5e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'crm_sync_records',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('institution_id', sa.UUID(), nullable=False),
        sa.Column('provider', sa.String(length=100), nullable=False),
        sa.Column('external_id', sa.String(length=255), nullable=True),
        sa.Column('status', sa.Enum('PENDING', 'SYNCED', 'FAILED', name='crmsyncstatus'), nullable=False),
        sa.Column('last_synced_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_error', sa.Text(), nullable=True),
        sa.Column('raw_response', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['institution_id'], ['canonical_institutions.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('institution_id', 'provider', name='uq_crm_sync_institution_provider'),
    )
    op.create_index(
        op.f('ix_crm_sync_records_institution_id'),
        'crm_sync_records', ['institution_id'], unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_crm_sync_records_institution_id'), table_name='crm_sync_records')
    op.drop_table('crm_sync_records')
    op.execute("DROP TYPE IF EXISTS crmsyncstatus")
