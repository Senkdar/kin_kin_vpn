from __future__ import annotations

import uuid
from decimal import Decimal

from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import BalanceTransaction, TelegramUser


async def create_deposit(
    session: AsyncSession,
    *,
    user_id: int,
    amount: Decimal,
    currency: str = "RUB",
) -> str:
    tx_id = str(uuid.uuid4())
    session.add(
        BalanceTransaction(
            id=tx_id,
            user_id=user_id,
            kind="topup",
            status="pending",
            amount=amount,
            currency=currency,
        )
    )
    await session.commit()
    return tx_id


async def confirm_deposit(
    session: AsyncSession,
    *,
    tx_id: str,
    user_id: int,
) -> bool:
    """
    Идемпотентное подтверждение: меняем pending->succeeded, иначе ничего не делаем.
    Возвращает True, если статус изменился на succeeded.
    """
    # 1) Меняем статус pending->succeeded и одновременно получаем сумму
    stmt = (
        update(BalanceTransaction)
        .where(
            BalanceTransaction.id == tx_id,
            BalanceTransaction.user_id == user_id,
            BalanceTransaction.kind == "topup",
            BalanceTransaction.status == "pending",
        )
        .values(status="succeeded")
        .returning(BalanceTransaction.amount)
        .execution_options(synchronize_session=False)
    )
    result = await session.execute(stmt)
    row = result.first()
    if row is None:
        await session.commit()
        return False
    amount: Decimal = row[0]
    # 2) Идемпотентно увеличиваем баланс пользователя
    inc_stmt = (
        update(TelegramUser)
        .where(TelegramUser.tg_user_id == user_id)
        .values(balance=TelegramUser.balance + amount)
        .execution_options(synchronize_session=False)
    )
    await session.execute(inc_stmt)
    await session.commit()
    return True


async def get_balance(session: AsyncSession, *, user_id: int) -> Decimal:
    """Получение баланса пользователя."""
    q = select(TelegramUser.balance).where(TelegramUser.tg_user_id == user_id)
    res = await session.execute(q)
    value = res.scalar_one_or_none()
    return value or Decimal("0.00")


