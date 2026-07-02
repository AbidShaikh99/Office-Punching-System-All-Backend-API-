"""add paid leave last added at to users

Revision ID: 2c4a8a5b6e11
Revises: f1c2d3e4b5a6
Create Date: 2026-06-23 17:40:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2c4a8a5b6e11'
down_revision: Union[str, Sequence[str], None] = 'f1c2d3e4b5a6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'users',
        sa.Column('paid_leave_last_added_at', sa.DateTime(), nullable=True),
    )

    op.execute(
        sa.text(
            "UPDATE users "
            "SET paid_leave_last_added_at = NOW() "
            "WHERE role = 'user'"
        )
    )


def downgrade() -> None:
    op.drop_column('users', 'paid_leave_last_added_at')
