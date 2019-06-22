"""empty message

Revision ID: 8b10243cf2ae
Revises: 77e1980a0269
Create Date: 2019-06-22 20:29:43.834439

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b10243cf2ae'
down_revision = '77e1980a0269'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('person', sa.Column('logged_in', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('person', 'logged_in')
    # ### end Alembic commands ###
