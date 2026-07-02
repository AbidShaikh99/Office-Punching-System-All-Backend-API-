"""fix users id sequence

Revision ID: a8d2f0e6c9b1
Revises: 1f6e2c7a9b44
Create Date: 2026-06-23 15:10:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a8d2f0e6c9b1'
down_revision: Union[str, Sequence[str], None] = '1f6e2c7a9b44'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        sa.text(
            "SELECT setval("
            "pg_get_serial_sequence('users', 'id'), "
            "(SELECT COALESCE(MAX(id), 1) FROM users), "
            "true"
            ")"
        )
    )


def downgrade() -> None:
    pass
