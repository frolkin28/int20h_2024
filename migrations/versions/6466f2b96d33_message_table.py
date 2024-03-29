"""message table

Revision ID: 6466f2b96d33
Revises: ef3a39b91320
Create Date: 2024-02-10 01:13:22.458115

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6466f2b96d33'
down_revision = 'ef3a39b91320'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.String(length=512), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('lot_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['lot_id'], ['lots.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('message')
    # ### end Alembic commands ###
