from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession


async def start_card_payment(session: AsyncSession, *, user_id: int, tx_id: str) -> str:
    # Тут будет создание платежа у эквайера (redirect_url/checkout_token).
    return (
        "Оплата картой (sandbox):\n"
        f"- Транзакция: {tx_id}\n"
        "- Здесь будет ссылка на checkout страницы, 3DS и т.д.\n"
        "- После интеграции вебхук подтвердит оплату и баланс пополнится."
    )



# from fastapi import FastAPI, Request, HTTPException
# from aiogram import Bot
# import os
# import hmac
# import hashlib
# from sqlalchemy.ext.asyncio import AsyncSession
# from models import Payment  # SQLAlchemy модель платежа
# from database import async_session

# app = FastAPI()
# bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))
# WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")  # секрет платёжного провайдера

# def verify_signature(request_body: bytes, signature: str) -> bool:
#     computed = hmac.new(WEBHOOK_SECRET.encode(), request_body, hashlib.sha256).hexdigest()
#     return hmac.compare_digest(computed, signature)

# @app.post("/payment-webhook")
# async def payment_webhook(request: Request):
#     body = await request.body()
#     signature = request.headers.get("X-Signature", "")

#     if not verify_signature(body, signature):
#         raise HTTPException(status_code=403, detail="Invalid signature")

#     data = await request.json()
#     user_id = data.get("user_id")
#     provider_payment_id = data.get("payment_id")
#     amount = data.get("amount")
#     status = data.get("status")  # success / failed

#     async with async_session() as session:
#         async with session.begin():
#             payment = await session.get(Payment, {"provider_payment_id": provider_payment_id})
#             if payment:
#                 payment.status = status
#             else:
#                 payment = Payment(
#                     user_id=user_id,
#                     amount=amount,
#                     status=status,
#                     provider_payment_id=provider_payment_id
#                 )
#                 session.add(payment)

#     # Асинхронная отправка уведомления пользователю
#     if status == "success":
#         await bot.send_message(user_id, f"Оплата {amount} ₽ прошла успешно!")
#     else:
#         await bot.send_message(user_id, f"Оплата {amount} ₽ не прошла. Попробуйте снова.")

#     return {"ok": True}
