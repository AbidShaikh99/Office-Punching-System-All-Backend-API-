"""add paid leave fields

Revision ID: 163371d66139
Revises: c9d8e7f6a5b4
Create Date: 2026-06-23 18:02:52.929433

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '163371d66139'
down_revision: Union[str, Sequence[str], None] = 'c9d8e7f6a5b4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        "users",
        sa.Column(
            "paid_leave",
            sa.Integer(),
            nullable=False,
            server_default="1"
        )
    )

    op.add_column(
        "users",
        sa.Column(
            "unpaid_leave",
            sa.Integer(),
            nullable=False,
            server_default="0"
        )
    )
