"""Add patentability assessment fields

Revision ID: 001_add_patentability
Revises:
Create Date: 2025-11-22 20:07:19.000000

This migration adds the new patentability assessment fields introduced in PRD v2.1.

These fields enable the system to assess whether a disclosure is patentable BEFORE
running the expensive prior art search, saving $500-1000 per avoided filing.
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001_add_patentability'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Add patentability assessment columns to analyses table."""
    # Add is_patentable column
    op.add_column('analyses', sa.Column('is_patentable', sa.Boolean(), nullable=True))

    # Add patentability_confidence column
    op.add_column('analyses', sa.Column('patentability_confidence', sa.Float(), nullable=True))

    # Add missing_elements column (JSON array stored as TEXT)
    op.add_column('analyses', sa.Column('missing_elements', sa.Text(), nullable=True))


def downgrade():
    """Remove patentability assessment columns."""
    op.drop_column('analyses', 'missing_elements')
    op.drop_column('analyses', 'patentability_confidence')
    op.drop_column('analyses', 'is_patentable')
