"""add orchestrate execution tracking fields

Revision ID: 002
Revises: 001
Create Date: 2025-11-22

This migration adds watsonx Orchestrate integration fields to the
orchestrate_logs table for tracking workflow executions.
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade():
    """Add orchestrate_execution_id and workflow_name fields."""
    # Add orchestrate_execution_id column
    op.add_column('orchestrate_logs',
        sa.Column('orchestrate_execution_id', sa.String(255), nullable=True)
    )

    # Add workflow_name column with default value
    op.add_column('orchestrate_logs',
        sa.Column('workflow_name', sa.String(100), nullable=True, server_default='patent-analysis-workflow')
    )

    # Create index on orchestrate_execution_id for faster lookups
    op.create_index(
        'idx_orchestrate_logs_execution_id',
        'orchestrate_logs',
        ['orchestrate_execution_id']
    )


def downgrade():
    """Remove orchestrate_execution_id and workflow_name fields."""
    # Drop index
    op.drop_index('idx_orchestrate_logs_execution_id', table_name='orchestrate_logs')

    # Drop columns
    op.drop_column('orchestrate_logs', 'workflow_name')
    op.drop_column('orchestrate_logs', 'orchestrate_execution_id')
