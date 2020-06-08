"""empty message

Revision ID: 349f509f5b9f
Revises: 2b25a581a459
Create Date: 2020-06-08 01:04:39.210150

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '349f509f5b9f'
down_revision = '2b25a581a459'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('present', sa.Column('date', sa.Date(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('present', 'date')
    # ### end Alembic commands ###