"""empty message

Revision ID: 3e19b4a212b6
Revises: cf6a127607a4
Create Date: 2020-05-27 01:53:47.080865

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e19b4a212b6'
down_revision = 'cf6a127607a4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('friend', sa.Column('address', sa.String(length=200), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('friend', 'address')
    # ### end Alembic commands ###