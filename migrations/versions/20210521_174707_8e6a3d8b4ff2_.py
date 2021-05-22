"""empty message

Revision ID: 8e6a3d8b4ff2
Revises: c618907185dd
Create Date: 2021-05-21 17:47:07.983371

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8e6a3d8b4ff2'
down_revision = 'c618907185dd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('repository',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('hosting_service_id', sa.Integer(), nullable=False),
    sa.Column('namespace', sa.String(length=500), nullable=False),
    sa.Column('name', sa.String(length=500), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('is_fork', sa.Boolean(), nullable=True),
    sa.Column('homepage', sa.String(length=500), nullable=True),
    sa.Column('language', sa.String(length=500), nullable=True),
    sa.Column('forks_count', sa.Integer(), nullable=False),
    sa.Column('stars_count', sa.Integer(), nullable=False),
    sa.Column('watchers_count', sa.Integer(), nullable=False),
    sa.Column('size', sa.Integer(), nullable=False),
    sa.Column('open_issues_count', sa.Integer(), nullable=False),
    sa.Column('is_archived', sa.Boolean(), nullable=True),
    sa.Column('is_disabled', sa.Boolean(), nullable=True),
    sa.Column('pushed_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('subscribers_', sa.DateTime(), nullable=True),
    sa.Column('subscribers_count', sa.Integer(), nullable=False),
    sa.Column('license_name', sa.String(length=500), nullable=True),
    sa.ForeignKeyConstraint(['hosting_service_id'], ['hosting_service.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.alter_column('hosting_service', 'label',
               existing_type=sa.VARCHAR(length=500),
               type_=sa.String(length=80),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('hosting_service', 'label',
               existing_type=sa.String(length=80),
               type_=sa.VARCHAR(length=500),
               existing_nullable=True)
    op.drop_table('repository')
    # ### end Alembic commands ###
