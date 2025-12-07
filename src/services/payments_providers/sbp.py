from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession


async def start_sbp_payment(session: AsyncSession, *, user_id: int, tx_id: str) -> str:
    # Тут будет генерация платежа у провайдера СБП (создание сессии, QR, deeplink и т.п.)
    return (
        "СБП (sandbox):\n"
        f"- Транзакция: {tx_id}\n"
        "- Здесь будет QR или ссылка на оплату.\n"
        "- После интеграции провайдер пришлёт вебхук, мы подтвердим зачисление."
    )


