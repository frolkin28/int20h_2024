"""<start price for lot>

Revision ID: 69c577410b04
Revises: 6466f2b96d33
Create Date: 2024-02-11 21:27:31.820396

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '69c577410b04'
down_revision = '6466f2b96d33'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('lots', schema=None) as batch_op:
        batch_op.add_column(sa.Column('start_price', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('lots', schema=None) as batch_op:
        batch_op.drop_column('start_price')

    # ### end Alembic commands ###
