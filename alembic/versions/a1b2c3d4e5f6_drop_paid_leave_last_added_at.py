"""drop paid leave last added at

Revision ID: a1b2c3d4e5f6
Revises: 2c4a8a5b6e11
Create Date: 2026-06-23 18:05:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = '2c4a8a5b6e11'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('users', 'paid_leave_last_added_at')


def downgrade() -> None:
    pass
