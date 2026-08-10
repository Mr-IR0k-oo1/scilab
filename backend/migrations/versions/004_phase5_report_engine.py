"""phase5_report_engine

Revision ID: 004_phase5
Revises: 003_phase4
Create Date: 2026-08-10 15:15:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '004_phase5'
down_revision: Union[str, None] = '003_phase4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'experiment_results',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('project_id', sa.String(length=36), nullable=False),
        sa.Column('experiment_id', sa.String(length=36), nullable=False),
        sa.Column('execution_id', sa.String(length=36), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='SUCCESS'),
        sa.Column('summary', sa.Text(), nullable=True),
        sa.Column('result_metadata', sa.Text(), nullable=False, server_default='{}'),
        sa.Column('artifact_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('schema_version', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['experiment_id'], ['experiments.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_experiment_results_project_id', 'experiment_results', ['project_id'])
    op.create_index('ix_experiment_results_experiment_id', 'experiment_results', ['experiment_id'])
    op.create_index('ix_experiment_results_execution_id', 'experiment_results', ['execution_id'])

    op.create_table(
        'result_artifacts',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('result_id', sa.String(length=36), nullable=False),
        sa.Column('type', sa.String(length=50), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('path', sa.String(length=1024), nullable=False),
        sa.Column('mime_type', sa.String(length=100), nullable=False, server_default='text/plain'),
        sa.Column('size', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('artifact_metadata', sa.Text(), nullable=False, server_default='{}'),
        sa.Column('hash', sa.String(length=64), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['result_id'], ['experiment_results.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_result_artifacts_result_id', 'result_artifacts', ['result_id'])

    op.create_table(
        'engineering_reports',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('project_id', sa.String(length=36), nullable=False),
        sa.Column('result_id', sa.String(length=36), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('author', sa.String(length=255), nullable=True),
        sa.Column('organization', sa.String(length=255), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('template', sa.String(length=100), nullable=False, server_default='default_engineering_report'),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='COMPLETED'),
        sa.Column('output_path', sa.String(length=1024), nullable=False),
        sa.Column('hash', sa.String(length=64), nullable=True),
        sa.Column('size_bytes', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('schema_version', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('reproducibility', sa.Text(), nullable=False, server_default='{}'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['result_id'], ['experiment_results.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_engineering_reports_project_id', 'engineering_reports', ['project_id'])
    op.create_index('ix_engineering_reports_result_id', 'engineering_reports', ['result_id'])


def downgrade() -> None:
    op.drop_table('engineering_reports')
    op.drop_table('result_artifacts')
    op.drop_table('experiment_results')
