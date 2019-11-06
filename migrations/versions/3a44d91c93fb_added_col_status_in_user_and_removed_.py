"""Added col status in user and removed col status from posts

Revision ID: 3a44d91c93fb
Revises: 488f93f973c3
Create Date: 2019-11-01 11:29:15.430744

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils

# revision identifiers, used by Alembic.
import insta_backend

revision = '3a44d91c93fb'
down_revision = '488f93f973c3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'status')
    op.add_column('user', sa.Column('status', sa.String(30), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'status')
    op.add_column('post', sa.Column('status', sa.VARCHAR(length=128),
                                    autoincrement=False, nullable=True))
    # ### end Alembic commands ###