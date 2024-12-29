"""hobbies

Revision ID: 3fb1added8d7
Revises: ac6845a722ee
Create Date: 2024-12-28 21:33:18.984965

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3fb1added8d7'
down_revision = 'ac6845a722ee'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('teacher')
    op.drop_table('achievement')
    op.drop_table('subject')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('subject',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('achievement',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('teacher',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.Column('surname', sa.VARCHAR(), nullable=True),
    sa.Column('students_class', sa.INTEGER(), nullable=True),
    sa.Column('school', sa.INTEGER(), nullable=True),
    sa.Column('feedback', sa.INTEGER(), nullable=True),
    sa.Column('about_text', sa.TEXT(), nullable=True),
    sa.Column('image', sa.VARCHAR(), nullable=True),
    sa.Column('subject_id', sa.INTEGER(), nullable=True),
    sa.Column('achievement_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['achievement_id'], ['achievement.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['subject_id'], ['subject.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
