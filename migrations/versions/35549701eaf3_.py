"""empty message

Revision ID: 35549701eaf3
Revises: 
Create Date: 2021-03-13 15:49:42.621092

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '35549701eaf3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('permissions', sa.UnicodeText(), nullable=True),
    sa.Column('update_datetime', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.Column('fs_uniquifier', sa.String(length=64), nullable=False),
    sa.Column('confirmed_at', sa.DateTime(), nullable=True),
    sa.Column('last_login_at', sa.DateTime(), nullable=True),
    sa.Column('current_login_at', sa.DateTime(), nullable=True),
    sa.Column('last_login_ip', sa.String(length=64), nullable=True),
    sa.Column('current_login_ip', sa.String(length=64), nullable=True),
    sa.Column('login_count', sa.Integer(), nullable=True),
    sa.Column('tf_primary_method', sa.String(length=64), nullable=True),
    sa.Column('tf_totp_secret', sa.String(length=255), nullable=True),
    sa.Column('tf_phone_number', sa.String(length=128), nullable=True),
    sa.Column('create_datetime', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('update_datetime', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=True),
    sa.Column('us_totp_secrets', sa.Text(), nullable=True),
    sa.Column('us_phone_number', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('fs_uniquifier'),
    sa.UniqueConstraint('username')
    )
    op.create_table('roles_users',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('roles_users')
    op.drop_table('user')
    op.drop_table('role')
    # ### end Alembic commands ###
