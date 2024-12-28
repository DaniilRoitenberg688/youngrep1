"""empty message

Revision ID: ac6845a722ee
Revises: ca53e80377ef
Create Date: 2024-12-28 18:01:35.209705

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac6845a722ee'
down_revision = 'ca53e80377ef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('teacher', schema=None) as batch_op:
        batch_op.alter_column('subject_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('achievement_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('teacher', schema=None) as batch_op:
        batch_op.alter_column('achievement_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('subject_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###
