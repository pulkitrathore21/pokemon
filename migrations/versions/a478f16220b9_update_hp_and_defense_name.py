"""update hp and defense name.

Revision ID: a478f16220b9
Revises: 5202133ec3cf
Create Date: 2023-06-08 22:54:52.701155

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a478f16220b9"
down_revision = "5202133ec3cf"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("pokemon_table", schema=None) as batch_op:
        batch_op.add_column(sa.Column("hp", sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column("defense", sa.Integer(), nullable=True))
        batch_op.drop_column("Defense")
        batch_op.drop_column("HP")

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("pokemon_table", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("HP", sa.INTEGER(), autoincrement=False, nullable=True)
        )
        batch_op.add_column(
            sa.Column("Defense", sa.INTEGER(), autoincrement=False, nullable=True)
        )
        batch_op.drop_column("defense")
        batch_op.drop_column("hp")

    # ### end Alembic commands ###
