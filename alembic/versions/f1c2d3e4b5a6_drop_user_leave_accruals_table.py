"""drop user leave accruals table

Revision ID: f1c2d3e4b5a6
Revises: 6c1dcbf5a2e4
Create Date: 2026-06-23 17:10:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'f1c2d3e4b5a6'
down_revision: Union[str, Sequence[str], None] = '6c1dcbf5a2e4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_table('user_leave_accruals')


def downgrade() -> None:
    pass
