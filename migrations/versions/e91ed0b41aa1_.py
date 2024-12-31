"""empty message

Revision ID: e91ed0b41aa1
Revises: 
Create Date: 2024-12-31 15:07:54.011562

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e91ed0b41aa1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contact_messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('subject', sa.String(length=100), nullable=False),
    sa.Column('message', sa.Text(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('contact_messages', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_contact_messages_email'), ['email'], unique=False)

    op.create_table('newsletter_subscribers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('roles', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_roles_name'), ['name'], unique=True)

    op.create_table('service_request',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('service_id', sa.String(length=255), nullable=False),
    sa.Column('service_title', sa.String(length=255), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('phone', sa.String(length=50), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('subscribe_to_newsletter', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=150), nullable=False),
    sa.Column('email', sa.String(length=150), nullable=False),
    sa.Column('password_hash', sa.String(length=256), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_users_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_users_username'), ['username'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_users_username'))
        batch_op.drop_index(batch_op.f('ix_users_email'))

    op.drop_table('users')
    op.drop_table('service_request')
    with op.batch_alter_table('roles', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_roles_name'))

    op.drop_table('roles')
    op.drop_table('newsletter_subscribers')
    with op.batch_alter_table('contact_messages', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_contact_messages_email'))

    op.drop_table('contact_messages')
    # ### end Alembic commands ###
