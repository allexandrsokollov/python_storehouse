"""empty message

Revision ID: 1ec373eddc8e
Revises: cf953a835937
Create Date: 2023-10-06 21:22:32.385088

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1ec373eddc8e"
down_revision: Union[str, None] = "cf953a835937"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("pallet", "location_id", existing_type=sa.UUID(), nullable=True)
    op.alter_column("pallet", "user_id", existing_type=sa.UUID(), nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("pallet", "user_id", existing_type=sa.UUID(), nullable=False)
    op.alter_column("pallet", "location_id", existing_type=sa.UUID(), nullable=False)
    # ### end Alembic commands ###
