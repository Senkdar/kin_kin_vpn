from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.navigation.stack import push as _push
from bot.views.menu import render

referrals_router = Router()


@referrals_router.callback_query(F.data == "menu_invite")
async def on_menu_invite(callback: CallbackQuery, state: FSMContext):
    await _push(state, "referrals", {})
    await render(callback, session=None, state=state)
    await callback.answer()


