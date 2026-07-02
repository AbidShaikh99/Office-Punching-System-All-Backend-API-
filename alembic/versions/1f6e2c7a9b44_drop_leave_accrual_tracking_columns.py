"""drop leave accrual tracking columns

Revision ID: 1f6e2c7a9b44
Revises: c31b8b2f1a90
Create Date: 2026-06-23 14:45:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1f6e2c7a9b44'
down_revision: Union[str, Sequence[str], None] = 'c31b8b2f1a90'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('users', 'last_leave_accrual_year')
    op.drop_column('users', 'last_leave_accrual_month')


def downgrade() -> None:
    op.add_column(
        'users',
        sa.Column(
            'last_leave_accrual_month',
            sa.Integer(),
            nullable=False,
            server_default=sa.text('0'),
        ),
    )
    op.add_column(
        'users',
        sa.Column(
            'last_leave_accrual_year',
            sa.Integer(),
            nullable=False,
            server_default=sa.text('0'),
        ),
    )
