"""add users.balance_minor

Revision ID: 20251206_add_users_balance
Revises: 20251206_add_balance_tx
Create Date: 2025-12-06
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20251206_add_users_balance"
down_revision = "20251206_add_balance_tx"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("balance", sa.BigInteger(), nullable=False, server_default="0"),
    )
    # server_default already sets 0 for existing rows


def downgrade() -> None:
    op.drop_column("users", "balance")


