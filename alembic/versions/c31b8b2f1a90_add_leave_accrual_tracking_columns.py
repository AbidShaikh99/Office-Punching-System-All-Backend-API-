"""add leave accrual tracking columns

Revision ID: c31b8b2f1a90
Revises: 380e29c6af46
Create Date: 2026-06-23 14:20:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c31b8b2f1a90'
down_revision: Union[str, Sequence[str], None] = '380e29c6af46'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
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

    op.execute(
        sa.text(
            "UPDATE users "
            "SET last_leave_accrual_month = EXTRACT(MONTH FROM CURRENT_DATE)::int, "
            "last_leave_accrual_year = EXTRACT(YEAR FROM CURRENT_DATE)::int"
        )
    )

    op.alter_column(
        'users',
        'last_leave_accrual_month',
        existing_type=sa.Integer(),
        server_default=None,
    )
    op.alter_column(
        'users',
        'last_leave_accrual_year',
        existing_type=sa.Integer(),
        server_default=None,
    )


def downgrade() -> None:
    op.drop_column('users', 'last_leave_accrual_year')
    op.drop_column('users', 'last_leave_accrual_month')
