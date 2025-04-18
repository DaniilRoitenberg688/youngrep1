"""page description

Revision ID: 4f3b42a9754c
Revises: 5c63aa6b7655
Create Date: 2025-01-27 16:56:35.416522

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f3b42a9754c'
down_revision = '5c63aa6b7655'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('page', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('page', schema=None) as batch_op:
        batch_op.drop_column('description')

    # ### end Alembic commands ###
