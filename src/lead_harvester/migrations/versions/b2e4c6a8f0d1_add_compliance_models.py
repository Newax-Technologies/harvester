"""Add compliance models (suppression, deletion requests, consent basis)

Revision ID: b2e4c6a8f0d1
Revises: a7c9d1e3f5b8
Create Date: 2026-07-31 02:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'b2e4c6a8f0d1'
down_revision: Union[str, Sequence[str], None] = 'a7c9d1e3f5b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

identifier_type_enum = sa.Enum('EMAIL', 'PHONE', 'DOMAIN', name='identifiertype', create_type=False)


def upgrade() -> None:
    """Upgrade schema."""
    identifier_type_enum.create(op.get_bind(), checkfirst=True)

    op.add_column(
        'contact_points',
        sa.Column(
            'consent_basis',
            sa.Enum('PUBLIC_DIRECTORY', 'LICENSED_EXPORT', 'OWNED_DATA', 'UNKNOWN', name='consentbasis'),
            nullable=False, server_default='UNKNOWN',
        ),
    )
    op.add_column('contact_points', sa.Column('consent_note', sa.Text(), nullable=False, server_default=''))

    op.create_table(
        'suppression_entries',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('identifier_type', identifier_type_enum, nullable=False),
        sa.Column('identifier_value', sa.String(length=255), nullable=False),
        sa.Column('reason', sa.Enum('UNSUBSCRIBED', 'BOUNCED', 'COMPLAINT', 'LEGAL_REQUEST', 'MANUAL', name='suppressionreason'), nullable=False),
        sa.Column('note', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('identifier_type', 'identifier_value', name='uq_suppression_identifier'),
    )
    op.create_index(op.f('ix_suppression_entries_identifier_value'), 'suppression_entries', ['identifier_value'], unique=False)

    op.create_table(
        'deletion_requests',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('identifier_type', identifier_type_enum, nullable=False),
        sa.Column('identifier_value', sa.String(length=255), nullable=False),
        sa.Column('status', sa.Enum('PENDING', 'COMPLETED', 'FAILED', name='deletionrequeststatus'), nullable=False),
        sa.Column('notes', sa.Text(), nullable=False),
        sa.Column('requested_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_deletion_requests_identifier_value'), 'deletion_requests', ['identifier_value'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_deletion_requests_identifier_value'), table_name='deletion_requests')
    op.drop_table('deletion_requests')
    op.execute("DROP TYPE IF EXISTS deletionrequeststatus")

    op.drop_index(op.f('ix_suppression_entries_identifier_value'), table_name='suppression_entries')
    op.drop_table('suppression_entries')
    op.execute("DROP TYPE IF EXISTS suppressionreason")

    op.drop_column('contact_points', 'consent_note')
    op.drop_column('contact_points', 'consent_basis')
    op.execute("DROP TYPE IF EXISTS consentbasis")

    identifier_type_enum.drop(op.get_bind(), checkfirst=True)
