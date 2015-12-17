"""empty message

Revision ID: 6ae1dcca019
Revises: 22059c8154eb
Create Date: 2015-12-17 12:06:48.976507

"""

# revision identifiers, used by Alembic.
revision = '6ae1dcca019'
down_revision = '22059c8154eb'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('admin', sa.Boolean(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'admin')
    ### end Alembic commands ###