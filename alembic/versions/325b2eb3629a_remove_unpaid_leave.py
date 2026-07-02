"""remove unpaid leave

Revision ID: 325b2eb3629a
Revises: 2e5af355519e
Create Date: 2026-06-24 16:21:57.398723

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '325b2eb3629a'
down_revision: Union[str, Sequence[str], None] = '2e5af355519e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None





def upgrade():
    op.drop_column("users", "unpaid_leave")


def downgrade():
    op.add_column(
        "users",
        sa.Column(
            "unpaid_leave",
            sa.Integer(),
            nullable=False,
            server_default="0"
        )
    )
