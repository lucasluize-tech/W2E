"""empty message

Revision ID: 540209e25f1d
Revises: f69a6dfd554a
Create Date: 2021-09-27 15:59:32.223483

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '540209e25f1d'
down_revision = 'f69a6dfd554a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('favs', 'timestamp')
    op.add_column('recipes', sa.Column('timestamp', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('recipes', 'timestamp')
    op.add_column('favs', sa.Column('timestamp', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
