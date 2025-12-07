from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards.menu import payments_amounts_kb
from bot.navigation.stack import push as _push
from bot.views.menu import render
from services.payments import confirm_topup_sandbox, make_deposit, start_deposit_process
from services.payments_providers.card import start_card_payment
from services.payments_providers.sbp import start_sbp_payment

payments_router = Router()


@payments_router.callback_query(F.data == "menu_pay")
async def on_menu_pay(callback: CallbackQuery, session: AsyncSession, state: FSMContext):
    await _push(state, "payments_overview", {})
    await render(callback, session=session, state=state)
    await callback.answer()


@payments_router.callback_query(F.data.startswith("pay_amount:"))
async def on_pay_amount(callback: CallbackQuery, session: AsyncSession, state: FSMContext):
    try:
        amount_rub = int(callback.data.split("pay_amount:", 1)[1])
        tx_id = await start_deposit_process(session, user_id=callback.from_user.id, amount_rub=amount_rub)
        await _push(state, "payments_methods", {"tx_id": tx_id, "amount_rub": amount_rub})
        await render(callback, session=session, state=state)
    except ValueError as e:
        await callback.answer(str(e), show_alert=True)
        return
    await callback.answer()


@payments_router.callback_query(F.data.startswith("pay_confirm:"))
async def on_pay_confirm(callback: CallbackQuery, session: AsyncSession):
    tx_id = callback.data.split("pay_confirm:", 1)[1]
    ok = await confirm_topup_sandbox(session, user_id=callback.from_user.id, tx_id=tx_id)
    suffix = "зачислены." if ok else "уже были зачислены или операция недоступна."
    text = await make_deposit(session, user_id=callback.from_user.id)
    await callback.message.edit_text(
        f"Оплата успешно подтверждена, средства {suffix}\n\n{text}",
        reply_markup=payments_amounts_kb(),
    )
    await callback.answer()


@payments_router.callback_query(F.data.startswith("pay_method:sbp:"))
async def on_pay_method_sbp(callback: CallbackQuery, session: AsyncSession, state: FSMContext):
    tx_id = callback.data.split("pay_method:sbp:", 1)[1]
    text = await start_sbp_payment(session, user_id=callback.from_user.id, tx_id=tx_id)
    await _push(state, "provider_intro", {"text": text})
    await render(callback, session=session, state=state)
    await callback.answer()


@payments_router.callback_query(F.data.startswith("pay_method:card:"))
async def on_pay_method_card(callback: CallbackQuery, session: AsyncSession, state: FSMContext):
    tx_id = callback.data.split("pay_method:card:", 1)[1]
    text = await start_card_payment(session, user_id=callback.from_user.id, tx_id=tx_id)
    await _push(state, "provider_intro", {"text": text})
    await render(callback, session=session, state=state)
    await callback.answer()


