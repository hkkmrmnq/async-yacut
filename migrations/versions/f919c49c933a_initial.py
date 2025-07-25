"""initial

Revision ID: f919c49c933a
Revises: 
Create Date: 2025-06-24 20:31:53.842807

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f919c49c933a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('url_map',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('original', sa.String(length=2048), nullable=False),
    sa.Column('short', sa.String(length=16), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('url_map', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_url_map_timestamp'), ['timestamp'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('url_map', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_url_map_timestamp'))

    op.drop_table('url_map')
    # ### end Alembic commands ###
