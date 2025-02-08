"""empty message

Revision ID: 6cccfb34581f
Revises: 613f538176df
Create Date: 2025-02-08 17:51:26.742632

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6cccfb34581f'
down_revision = '613f538176df'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('teacher', schema=None) as batch_op:
        batch_op.add_column(sa.Column('shown_times', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('teacher', schema=None) as batch_op:
        batch_op.drop_column('shown_times')

    # ### end Alembic commands ###
