"""drop user leave accruals table

Revision ID: 0c7b6f3a12de
Revises: b8a4a1d6c2f7
Create Date: 2026-06-23 16:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '0c7b6f3a12de'
down_revision: Union[str, Sequence[str], None] = 'b8a4a1d6c2f7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_table('user_leave_accruals')


def downgrade() -> None:
    op.execute(
        """
        CREATE TABLE user_leave_accruals (
            id SERIAL NOT NULL PRIMARY KEY,
            user_id INTEGER NOT NULL UNIQUE REFERENCES users(id),
            last_accrual_month INTEGER NOT NULL DEFAULT 0,
            last_accrual_year INTEGER NOT NULL DEFAULT 0,
            created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
