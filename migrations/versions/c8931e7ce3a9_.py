"""empty message

Revision ID: c8931e7ce3a9
Revises: 540209e25f1d
Create Date: 2021-09-30 16:14:47.356507

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c8931e7ce3a9'
down_revision = '540209e25f1d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('recipes', sa.Column('image_url', sa.Text(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('recipes', 'image_url')
    # ### end Alembic commands ###
