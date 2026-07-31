"""Add contact verification models

Revision ID: f1a2b3c4d5e6
Revises: b007b9280dac
Create Date: 2026-07-31 00:54:14.492543

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'f1a2b3c4d5e6'
down_revision: Union[str, Sequence[str], None] = 'b007b9280dac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Shared across two columns in this migration, so we create it once explicitly
# and reference it with create_type=False everywhere else to avoid a duplicate
# "CREATE TYPE" attempt.
verification_status_enum = postgresql.ENUM(
    'PENDING', 'VALID', 'INVALID', 'RISKY', 'UNKNOWN',
    name='verificationstatus',
    create_type=False,
)


def upgrade() -> None:
    """Upgrade schema."""
    verification_status_enum.create(op.get_bind(), checkfirst=True)

    op.add_column(
        'contact_points',
        sa.Column('verification_status', verification_status_enum, nullable=False, server_default='PENDING'),
    )
    op.add_column('contact_points', sa.Column('verified_at', sa.DateTime(timezone=True), nullable=True))

    op.create_table(
        'contact_verifications',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('contact_point_id', sa.UUID(), nullable=False),
        sa.Column('provider', sa.String(length=100), nullable=False),
        sa.Column('status', verification_status_enum, nullable=False),
        sa.Column('is_disposable', sa.Boolean(), nullable=False),
        sa.Column('is_role_account', sa.Boolean(), nullable=False),
        sa.Column('mx_found', sa.Boolean(), nullable=True),
        sa.Column('raw_response', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('verified_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['contact_point_id'], ['contact_points.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(
        op.f('ix_contact_verifications_contact_point_id'),
        'contact_verifications', ['contact_point_id'], unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_contact_verifications_contact_point_id'), table_name='contact_verifications')
    op.drop_table('contact_verifications')

    op.drop_column('contact_points', 'verified_at')
    op.drop_column('contact_points', 'verification_status')

    verification_status_enum.drop(op.get_bind(), checkfirst=True)
