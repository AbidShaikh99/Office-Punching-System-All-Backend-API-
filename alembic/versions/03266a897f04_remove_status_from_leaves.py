"""remove status from leaves

Revision ID: 03266a897f04
Revises: 9cb048f1d7b4
Create Date: 2026-06-22 18:37:32.952022

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '03266a897f04'
down_revision: Union[str, Sequence[str], None] = '9cb048f1d7b4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None





def upgrade():
    op.drop_column("leaves", "status")


def downgrade():
    op.add_column(
        "leaves",
        sa.Column(
            "status",
            sa.String(),
            nullable=True
        )
    )
