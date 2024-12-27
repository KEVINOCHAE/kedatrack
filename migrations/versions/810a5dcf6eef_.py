"""empty message

Revision ID: 810a5dcf6eef
Revises: 
Create Date: 2024-12-27 12:11:07.986054

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '810a5dcf6eef'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
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
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('service_request')
    # ### end Alembic commands ###
