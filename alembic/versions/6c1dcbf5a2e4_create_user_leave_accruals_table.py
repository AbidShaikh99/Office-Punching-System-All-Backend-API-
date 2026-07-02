"""create user leave accruals table

Revision ID: 6c1dcbf5a2e4
Revises: 4a9f1d7c8e21
Create Date: 2026-06-23 16:45:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision: str = '6c1dcbf5a2e4'
down_revision: Union[str, Sequence[str], None] = '4a9f1d7c8e21'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)

    if not inspector.has_table('user_leave_accruals'):
        op.create_table(
            'user_leave_accruals',
            sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
            sa.Column('user_id', sa.Integer(), nullable=False),
            sa.Column('last_accrual_month', sa.Integer(), nullable=False, server_default=sa.text('0')),
            sa.Column('last_accrual_year', sa.Integer(), nullable=False, server_default=sa.text('0')),
            sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
            sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
            sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('user_leave_accruals_user_id_fkey')),
            sa.PrimaryKeyConstraint('id', name=op.f('user_leave_accruals_pkey')),
            sa.UniqueConstraint('user_id', name=op.f('user_leave_accruals_user_id_key')),
        )

    op.execute(
        sa.text(
            "INSERT INTO user_leave_accruals (user_id, last_accrual_month, last_accrual_year, created_at, updated_at) "
            "SELECT id, EXTRACT(MONTH FROM CURRENT_DATE)::int, EXTRACT(YEAR FROM CURRENT_DATE)::int, NOW(), NOW() "
            "FROM users "
            "ON CONFLICT (user_id) DO NOTHING"
        )
    )

    op.alter_column(
        'user_leave_accruals',
        'last_accrual_month',
        server_default=None,
        existing_type=sa.Integer(),
    )
    op.alter_column(
        'user_leave_accruals',
        'last_accrual_year',
        server_default=None,
        existing_type=sa.Integer(),
    )
    op.alter_column(
        'user_leave_accruals',
        'created_at',
        server_default=None,
        existing_type=sa.DateTime(),
    )
    op.alter_column(
        'user_leave_accruals',
        'updated_at',
        server_default=None,
        existing_type=sa.DateTime(),
    )


def downgrade() -> None:
    op.drop_table('user_leave_accruals')
