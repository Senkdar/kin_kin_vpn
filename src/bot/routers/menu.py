from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.keyboards.menu import main_menu_kb
from bot.navigation.stack import pop as _pop
from bot.navigation.stack import push as _push
from bot.navigation.stack import set_stack as _set_stack
from bot.views.menu import render as _render

menu_router = Router()


@menu_router.message(Command("menu"))
async def menu(message: Message, state: FSMContext):
    await _set_stack(state, [])
    await _push(state, "main", {})
    await message.answer("Выберите действие:", reply_markup=main_menu_kb())


@menu_router.callback_query(F.data == "menu_back")
async def on_menu_back(callback: CallbackQuery, state: FSMContext):
    await _set_stack(state, [])
    await _push(state, "main", {})
    await _render(callback, session=None, state=state)
    await callback.answer()


@menu_router.callback_query(F.data == "nav_back")
async def on_nav_back(callback: CallbackQuery, state: FSMContext):
    await _pop(state)
    await _render(callback, session=None, state=state)
    await callback.answer()


@menu_router.callback_query(F.data == "nav_home")
async def on_nav_home(callback: CallbackQuery, state: FSMContext):
    await _set_stack(state, [])
    await _push(state, "main", {})
    await _render(callback, session=None, state=state)
    await callback.answer()


