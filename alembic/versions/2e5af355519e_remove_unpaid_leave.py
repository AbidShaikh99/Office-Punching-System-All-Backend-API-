"""remove unpaid leave

Revision ID: 2e5af355519e
Revises: e77b9b4fd546
Create Date: 2026-06-24 16:20:25.901197

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2e5af355519e'
down_revision: Union[str, Sequence[str], None] = 'e77b9b4fd546'
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
