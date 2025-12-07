"""add balance_transactions

Revision ID: 20251206_add_balance_tx
Revises: a876aa47475f
Create Date: 2025-12-06
"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "20251206_add_balance_tx"
down_revision = "a876aa47475f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "balance_transactions",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("user_id", sa.BigInteger(), sa.ForeignKey("users.tg_user_id", ondelete="CASCADE"), nullable=False),
        sa.Column("kind", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("amount_minor", sa.Integer(), nullable=False),
        sa.Column("currency", sa.String(length=8), nullable=False, server_default="RUB"),
        sa.Column("external_id", sa.String(length=128), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.CheckConstraint("amount_minor > 0", name="chk_amount_positive"),
        sa.CheckConstraint("status in ('pending','succeeded','canceled')", name="chk_status_valid"),
        sa.CheckConstraint("kind in ('topup')", name="chk_kind_valid"),
    )
    op.create_index("ix_balance_tx_user_id", "balance_transactions", ["user_id"])


def downgrade() -> None:
    op.drop_index("ix_balance_tx_user_id", table_name="balance_transactions")
    op.drop_table("balance_transactions")


