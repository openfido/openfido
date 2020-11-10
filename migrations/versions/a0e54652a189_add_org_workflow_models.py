"""add_org_workflow_models

Revision ID: a0e54652a189
Revises: e53a1b7d4c64
Create Date: 2020-11-10 16:15:02.067607

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a0e54652a189'
down_revision = 'e53a1b7d4c64'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('organization_workflow',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.String(length=32), server_default='', nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('organization_uuid', sa.String(length=32), server_default='', nullable=False),
    sa.Column('workflow_uuid', sa.String(length=32), server_default='', nullable=False),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('organization_workflow_pipeline',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.String(length=32), server_default='', nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('organization_workflow_uuid', sa.String(length=32), server_default='', nullable=False),
    sa.Column('organization_pipeline_id', sa.Integer(), nullable=False),
    sa.Column('workflow_pipeline_uuid', sa.String(length=32), server_default='', nullable=False),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['organization_pipeline_id'], ['organization_pipeline.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('organization_workflow_pipeline_run',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.String(length=32), server_default='', nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('organization_workflow_id', sa.Integer(), nullable=False),
    sa.Column('organization_pipeline_run_id', sa.Integer(), nullable=False),
    sa.Column('workflow_run_uuid', sa.String(length=32), server_default='', nullable=False),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['organization_pipeline_run_id'], ['organization_pipeline_run.id'], ),
    sa.ForeignKeyConstraint(['organization_workflow_id'], ['organization_workflow.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('organization_workflow_pipeline_run')
    op.drop_table('organization_workflow_pipeline')
    op.drop_table('organization_workflow')
    # ### end Alembic commands ###
