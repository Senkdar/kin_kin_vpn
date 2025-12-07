from __future__ import annotations

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards.devices import devices_add_kb, devices_list_kb
from bot.keyboards.menu import (
    back_kb,
    main_menu_kb,
    payments_amounts_kb,
    payments_methods_kb,
)
from bot.navigation.stack import current as nav_current
from services.devices import describe_devices, intro_add_device
from services.payments import make_deposit
from services.referrals import describe_referrals


async def render_main(callback: CallbackQuery, *, session: AsyncSession | None, state: FSMContext, payload: dict) -> None:
    await callback.message.edit_text("Выберите действие:", reply_markup=main_menu_kb())


async def render_payments_overview(callback: CallbackQuery, *, session: AsyncSession | None, state: FSMContext, payload: dict) -> None:
    user_id = callback.from_user.id if callback.from_user else None
    text = await make_deposit(session, user_id=user_id)
    await callback.message.edit_text(text, reply_markup=payments_amounts_kb())


async def render_payments_methods(callback: CallbackQuery, *, session: AsyncSession | None, state: FSMContext, payload: dict) -> None:
    amount_rub = payload.get("amount_rub")
    tx_id = payload.get("tx_id", "")
    txt = "Выберите способ оплаты:" if amount_rub is None else f"Вы выбрали пополнение на {amount_rub} ₽.\nВыберите способ оплаты:"
    await callback.message.edit_text(txt, reply_markup=payments_methods_kb(tx_id))


async def render_provider_intro(callback: CallbackQuery, *, session: AsyncSession | None, state: FSMContext, payload: dict) -> None:
    txt = payload.get("text", "Оплата")
    await callback.message.edit_text(txt, reply_markup=back_kb())


async def render_devices(callback: CallbackQuery, *, session: AsyncSession | None, state: FSMContext, payload: dict) -> None:
    text = await describe_devices()
    await callback.message.edit_text(text, reply_markup=devices_list_kb())


async def render_devices_add(callback: CallbackQuery, *, session: AsyncSession | None, state: FSMContext, payload: dict) -> None:
    text = await intro_add_device()
    await callback.message.edit_text(text, reply_markup=devices_add_kb())


async def render_referrals(callback: CallbackQuery, *, session: AsyncSession | None, state: FSMContext, payload: dict) -> None:
    text = await describe_referrals()
    await callback.message.edit_text(text, reply_markup=back_kb())


RENDERERS: dict[str, callable] = {
    "main": render_main,
    "payments_overview": render_payments_overview,
    "payments_methods": render_payments_methods,
    "provider_intro": render_provider_intro,
    "devices": render_devices,
    "devices_add": render_devices_add,
    "referrals": render_referrals,
}


async def render(callback: CallbackQuery, *, session: AsyncSession | None, state: FSMContext) -> None:
    entry = await nav_current(state)
    name = entry["name"]
    payload = entry.get("payload", {})
    handler = RENDERERS.get(name)
    await handler(callback, session=session, state=state, payload=payload)


