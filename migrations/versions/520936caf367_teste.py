"""teste

Revision ID: 520936caf367
Revises: 
Create Date: 2024-10-05 20:18:45.154520

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '520936caf367'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('usuarios', schema=None) as batch_op:
        batch_op.add_column(sa.Column('teste', sa.String(length=150), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('usuarios', schema=None) as batch_op:
        batch_op.drop_column('teste')

    # ### end Alembic commands ###
