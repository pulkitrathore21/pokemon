"""updating type 2

Revision ID: e809fcc52066
Revises: 5c776f02d804
Create Date: 2023-05-31 15:02:50.716444

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e809fcc52066"
down_revision = "5c776f02d804"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("pokemon_table", schema=None) as batch_op:
        batch_op.alter_column(
            "type_2", existing_type=sa.VARCHAR(length=100), nullable=True
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("pokemon_table", schema=None) as batch_op:
        batch_op.alter_column(
            "type_2", existing_type=sa.VARCHAR(length=100), nullable=False
        )

    # ### end Alembic commands ###
