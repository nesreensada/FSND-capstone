"""empty message

Revision ID: e234b8e8f2fe
Revises: 
Create Date: 2021-02-18 16:52:38.050426

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e234b8e8f2fe'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cast')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cast',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('actor_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('movie_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['actor_id'], ['actors.id'], name='cast_actor_id_fkey'),
    sa.ForeignKeyConstraint(['movie_id'], ['movies.id'], name='cast_movie_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='cast_pkey')
    )
    # ### end Alembic commands ###
