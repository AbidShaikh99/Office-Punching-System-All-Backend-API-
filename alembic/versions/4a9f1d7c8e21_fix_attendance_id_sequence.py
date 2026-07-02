"""fix attendance id sequence

Revision ID: 4a9f1d7c8e21
Revises: 0c7b6f3a12de
Create Date: 2026-06-23 16:20:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4a9f1d7c8e21'
down_revision: Union[str, Sequence[str], None] = '0c7b6f3a12de'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        sa.text(
            "SELECT setval("
            "pg_get_serial_sequence('attendance', 'id'), "
            "(SELECT COALESCE(MAX(id), 1) FROM attendance), "
            "true"
            ")"
        )
    )


def downgrade() -> None:
    pass
