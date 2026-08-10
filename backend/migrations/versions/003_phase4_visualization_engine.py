"""phase4_visualization_engine

Revision ID: 003_phase4
Revises: 002_phase3
Create Date: 2026-08-10 15:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '003_phase4'
down_revision: Union[str, None] = '002_phase3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('datasets_metadata', sa.Column('content_hash', sa.String(length=64), nullable=True))

    op.create_table(
        'visualizations',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('project_id', sa.String(length=36), nullable=False),
        sa.Column('dataset_id', sa.String(length=36), nullable=False),
        sa.Column('experiment_id', sa.String(length=36), nullable=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('type', sa.String(length=50), nullable=False),
        sa.Column('x_column', sa.String(length=255), nullable=True),
        sa.Column('y_columns', sa.Text(), nullable=False),
        sa.Column('group_column', sa.String(length=255), nullable=True),
        sa.Column('transformations', sa.Text(), nullable=False),
        sa.Column('options', sa.Text(), nullable=False),
        sa.Column('schema_version', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('dataset_hash', sa.String(length=64), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['dataset_id'], ['datasets_metadata.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['experiment_id'], ['experiments.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_visualizations_project_id', 'visualizations', ['project_id'])
    op.create_index('ix_visualizations_dataset_id', 'visualizations', ['dataset_id'])
    op.create_index('ix_visualizations_experiment_id', 'visualizations', ['experiment_id'])


def downgrade() -> None:
    op.drop_table('visualizations')
    op.drop_column('datasets_metadata', 'content_hash')
