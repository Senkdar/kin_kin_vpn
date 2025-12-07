from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.keyboards.menu import main_menu_kb, back_kb, devices_kb, payments_amounts_kb, payments_methods_kb
from services.payments import make_deposit, start_deposit_process, confirm_topup_sandbox
from services.referrals import describe_referrals
from services.devices import describe_devices, add_device
from sqlalchemy.ext.asyncio import AsyncSession
from services.payments_providers.sbp import start_sbp_payment
from services.payments_providers.card import start_card_payment

menu_router = Router()

async def _get_stack(state: FSMContext) -> list:
    data = await state.get_data()
    return list(data.get("nav_stack", []))

async def _set_stack(state: FSMContext, stack: list) -> None:
    await state.update_data(nav_stack=stack)

async def _push(state: FSMContext, name: str, payload: dict | None = None) -> None:
    stack = await _get_stack(state)
    stack.append({"name": name, "payload": payload or {}})
    await _set_stack(state, stack)

async def _pop(state: FSMContext) -> dict:
    stack = await _get_stack(state)
    if stack:
        stack.pop()
    await _set_stack(state, stack)
    return stack[-1] if stack else {"name": "main", "payload": {}}

async def _current(state: FSMContext) -> dict:
    stack = await _get_stack(state)
    return stack[-1] if stack else {"name": "main", "payload": {}}

async def _render(callback: CallbackQuery, *, session: AsyncSession | None, state: FSMContext) -> None:
    entry = await _current(state)
    name = entry["name"]
    payload = entry.get("payload", {})
    if name == "main":
        await callback.message.edit_text("Выберите действие:", reply_markup=main_menu_kb())
        return
    if name == "payments_overview":
        user_id = callback.from_user.id if callback.from_user else None
        text = await make_deposit(session, user_id=user_id)
        await callback.message.edit_text(text, reply_markup=payments_amounts_kb())
        return
    if name == "payments_methods":
        amount_rub = payload.get("amount_rub")
        tx_id = payload.get("tx_id", "")
        txt = "Выберите способ оплаты:" if amount_rub is None else f"Вы выбрали пополнение на {amount_rub} ₽.\nВыберите способ оплаты:"
        await callback.message.edit_text(txt, reply_markup=payments_methods_kb(tx_id))
        return
    if name == "provider_intro":
        txt = payload.get("text", "Оплата")
        await callback.message.edit_text(txt, reply_markup=back_kb())
        return
    if name == "devices":
        text = await describe_devices()
        await callback.message.edit_text(text, reply_markup=devices_kb())
        return
    if name == "referrals":
        text = await describe_referrals()
        await callback.message.edit_text(text, reply_markup=back_kb())
        return
    await callback.message.edit_text("Выберите действие:", reply_markup=main_menu_kb())


@menu_router.message(Command("menu"))
async def menu(message: Message, state: FSMContext):
    await _set_stack(state, [])
    await _push(state, "main", {})
    await message.answer("Выберите действие:", reply_markup=main_menu_kb())


@menu_router.callback_query(F.data == "menu_pay")
async def on_menu_pay(callback: CallbackQuery, session: AsyncSession, state: FSMContext):
    """Пополнить баланс."""
    await _push(state, "payments_overview", {})
    await _render(callback, session=session, state=state)
    await callback.answer()


@menu_router.callback_query(F.data == "menu_invite")
async def on_menu_invite(callback: CallbackQuery, state: FSMContext):
    """Пригласить друга."""
    await _push(state, "referrals", {})
    await _render(callback, session=None, state=state)
    await callback.answer()


@menu_router.callback_query(F.data == "menu_devices")
async def on_menu_devices(callback: CallbackQuery, state: FSMContext):
    """Мои устройства."""
    await _push(state, "devices", {})
    await _render(callback, session=None, state=state)
    await callback.answer()


@menu_router.callback_query(F.data == "add_device")
async def on_add_device(callback: CallbackQuery, state: FSMContext):
    """Добавить устройство."""
    await _push(state, "provider_intro", {"text": await add_device()})
    await _render(callback, session=None, state=state)
    await callback.answer()


@menu_router.callback_query(F.data == "menu_back")
async def on_menu_back(callback: CallbackQuery, state: FSMContext):
    await _set_stack(state, [])
    await _push(state, "main", {})
    await _render(callback, session=None, state=state)
    await callback.answer()


@menu_router.callback_query(F.data.startswith("pay_amount:"))
async def on_pay_amount(callback: CallbackQuery, session: AsyncSession, state: FSMContext):
    """Создаём платеж на выбранную сумму и предлагаем подтвердить (sandbox)."""

    try:
        amount_rub = int(callback.data.split("pay_amount:", 1)[1])
        tx_id = await start_deposit_process(session, user_id=callback.from_user.id, amount_rub=amount_rub)
        await _push(state, "payments_methods", {"tx_id": tx_id, "amount_rub": amount_rub})
        await _render(callback, session=session, state=state)
    except ValueError as e:
        await callback.answer(str(e), show_alert=True)
        return
    await callback.answer()


@menu_router.callback_query(F.data.startswith("pay_confirm:"))
async def on_pay_confirm(callback: CallbackQuery, session: AsyncSession):
    """
    Подтверждение платежа в песочнице: меняем статус на succeeded и обновляем баланс.
    """
    tx_id = callback.data.split("pay_confirm:", 1)[1]
    ok = await confirm_topup_sandbox(session, user_id=callback.from_user.id, tx_id=tx_id)
    suffix = "зачислены." if ok else "уже были зачислены или операция недоступна."
    text = await make_deposit(session, user_id=callback.from_user.id)
    await callback.message.edit_text(f"Оплата успешно подтверждена, средства {suffix}\n\n{text}", reply_markup=payments_amounts_kb())
    await callback.answer()

@menu_router.callback_query(F.data == "nav_back")
async def on_nav_back(callback: CallbackQuery, session: AsyncSession, state: FSMContext):
    await _pop(state)
    await _render(callback, session=session, state=state)
    await callback.answer()

@menu_router.callback_query(F.data == "nav_home")
async def on_nav_home(callback: CallbackQuery, session: AsyncSession, state: FSMContext):
    await _set_stack(state, [])
    await _push(state, "main", {})
    await _render(callback, session=session, state=state)
    await callback.answer()

@menu_router.callback_query(F.data.startswith("pay_method:sbp:"))
async def on_pay_method_sbp(callback: CallbackQuery, session: AsyncSession, state: FSMContext):
    tx_id = callback.data.split("pay_method:sbp:", 1)[1]
    text = await start_sbp_payment(session, user_id=callback.from_user.id, tx_id=tx_id)
    await _push(state, "provider_intro", {"text": text})
    await _render(callback, session=session, state=state)
    await callback.answer()

@menu_router.callback_query(F.data.startswith("pay_method:card:"))
async def on_pay_method_card(callback: CallbackQuery, session: AsyncSession, state: FSMContext):
    tx_id = callback.data.split("pay_method:card:", 1)[1]
    text = await start_card_payment(session, user_id=callback.from_user.id, tx_id=tx_id)
    await _push(state, "provider_intro", {"text": text})
    await _render(callback, session=session, state=state)
    await callback.answer()


