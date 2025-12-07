from __future__ import annotations

from decimal import Decimal
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from db.repos.payments import confirm_deposit, create_deposit, get_balance


async def make_deposit(session: Optional[AsyncSession] = None, *, user_id: Optional[int] = None) -> str:
    if session is None or user_id is None:
        return "Пополнение баланса. Выберите сумму."
    balance = await get_balance(session, user_id=user_id)
    return f"Баланс: {balance:.2f} ₽\nВыберите сумму пополнения:"


def validate_amount_rub(amount_rub: int) -> Decimal:
    # Правила: min=50₽, max=10000₽, кратно 10.
    if amount_rub < 50 or amount_rub > 10000 or amount_rub % 10 != 0:
        raise ValueError("Некорректная сумма. Допустимо: 50–10000₽, кратно 10.")
    return Decimal(amount_rub).quantize(Decimal("0.01"))


async def start_deposit_process(session: AsyncSession, *, user_id: int, amount_rub: int) -> str:
    amount = validate_amount_rub(amount_rub)
    tx_id = await create_deposit(session, user_id=user_id, amount=amount, currency="RUB")
    return tx_id


async def confirm_topup_sandbox(session: AsyncSession, *, user_id: int, tx_id: str) -> bool:
    return await confirm_deposit(session, tx_id=tx_id, user_id=user_id)


