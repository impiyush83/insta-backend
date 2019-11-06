"""Deleted status col in like table

Revision ID: 180046a31cb3
Revises: 3a44d91c93fb
Create Date: 2019-11-02 06:52:55.450654

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = '180046a31cb3'
down_revision = '3a44d91c93fb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('like', 'status')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('like', sa.Column('status', sa.String(length=128),
                                    autoincrement=False, nullable=False))
    # ### end Alembic commands ###