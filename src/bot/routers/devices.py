from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.navigation.stack import push as _push
from bot.views.menu import render
from services.devices import (
    describe_platform_android,
    describe_platform_mac,
    describe_platform_windows,
)

devices_router = Router()


@devices_router.callback_query(F.data == "menu_devices")
async def on_menu_devices(callback: CallbackQuery, state: FSMContext):
    await _push(state, "devices", {})
    await render(callback, session=None, state=state)
    await callback.answer()


@devices_router.callback_query(F.data == "add_device")
async def on_add_device(callback: CallbackQuery, state: FSMContext):
    await _push(state, "devices_add", {})
    await render(callback, session=None, state=state)
    await callback.answer()


@devices_router.callback_query(F.data == "dev_platform:mac")
async def on_dev_platform_mac(callback: CallbackQuery, state: FSMContext):
    await _push(state, "provider_intro", {"text": await describe_platform_mac()})
    await render(callback, session=None, state=state)
    await callback.answer()


@devices_router.callback_query(F.data == "dev_platform:android")
async def on_dev_platform_android(callback: CallbackQuery, state: FSMContext):
    await _push(state, "provider_intro", {"text": await describe_platform_android()})
    await render(callback, session=None, state=state)
    await callback.answer()


@devices_router.callback_query(F.data == "dev_platform:windows")
async def on_dev_platform_windows(callback: CallbackQuery, state: FSMContext):
    await _push(state, "provider_intro", {"text": await describe_platform_windows()})
    await render(callback, session=None, state=state)
    await callback.answer()


