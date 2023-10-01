"""f

Revision ID: 836cc2727556
Revises: 1f8815f84e0c
Create Date: 2023-10-01 12:30:17.322330

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '836cc2727556'
down_revision: Union[str, None] = '1f8815f84e0c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
