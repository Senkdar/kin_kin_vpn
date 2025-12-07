"""rename amount_minor->amount and convert to NUMERIC, users.balance to NUMERIC

Revision ID: 20251207_amount_decimal
Revises: 20251206_add_users_balance
Create Date: 2025-12-07
"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "20251207_amount_decimal"
down_revision = "20251206_add_users_balance"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # balance_transactions: rename amount_minor -> amount
    with op.batch_alter_table("balance_transactions") as batch_op:
        # Rename column if exists
        batch_op.alter_column("amount_minor", new_column_name="amount", existing_type=sa.Integer())
        # Convert to NUMERIC(18,2)
        batch_op.alter_column(
            "amount",
            type_=sa.Numeric(18, 2),
            existing_type=sa.Integer(),
            postgresql_using="amount::numeric",
            existing_nullable=False,
        )
        # Fix check constraint name and expression
        try:
            batch_op.drop_constraint("chk_amount_positive", type_="check")
        except Exception:
            pass
        batch_op.create_check_constraint("chk_amount_positive", "amount > 0")

    # users.balance: convert to NUMERIC(18,2)
    with op.batch_alter_table("users") as batch_op:
        batch_op.alter_column(
            "balance",
            type_=sa.Numeric(18, 2),
            existing_type=sa.BigInteger(),
            postgresql_using="balance::numeric",
            existing_nullable=False,
            server_default="0",
        )


def downgrade() -> None:
    # users.balance back to BIGINT
    with op.batch_alter_table("users") as batch_op:
        batch_op.alter_column(
            "balance",
            type_=sa.BigInteger(),
            existing_type=sa.Numeric(18, 2),
            postgresql_using="round(balance)::bigint",
            existing_nullable=False,
            server_default="0",
        )

    # balance_transactions.amount back to amount_minor INT
    with op.batch_alter_table("balance_transactions") as batch_op:
        try:
            batch_op.drop_constraint("chk_amount_positive", type_="check")
        except Exception:
            pass
        batch_op.alter_column(
            "amount",
            type_=sa.Integer(),
            existing_type=sa.Numeric(18, 2),
            postgresql_using="round(amount)::integer",
            existing_nullable=False,
        )
        batch_op.alter_column("amount", new_column_name="amount_minor", existing_type=sa.Integer())
        batch_op.create_check_constraint("chk_amount_positive", "amount_minor > 0")


