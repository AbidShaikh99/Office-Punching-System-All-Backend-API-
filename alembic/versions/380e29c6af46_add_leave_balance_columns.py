"""add leave balance columns

Revision ID: 380e29c6af46
Revises: 543ffe58ee5b
Create Date: 2026-06-23 12:06:43.702609

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '380e29c6af46'
down_revision: Union[str, Sequence[str], None] = '543ffe58ee5b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column(
        "users",
        "paid_leave_balance",
        existing_type=sa.Integer(),
        server_default=None,
    )
    op.alter_column(
        "users",
        "unpaid_leave_count",
        existing_type=sa.Integer(),
        server_default=None,
    )


def downgrade():
    op.alter_column(
        "users",
        "paid_leave_balance",
        existing_type=sa.Integer(),
        server_default=sa.text("0"),
    )
    op.alter_column(
        "users",
        "unpaid_leave_count",
        existing_type=sa.Integer(),
        server_default=sa.text("0"),
    )
