"""empty message

Revision ID: f69a6dfd554a
Revises: 384626019f15
Create Date: 2021-09-27 15:14:42.836201

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f69a6dfd554a'
down_revision = '384626019f15'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('image_url', sa.Text(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'image_url')
    # ### end Alembic commands ###
