from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards.menu import main_menu_kb
from services.users import save_user_if_new

start_router = Router()


@start_router.message(CommandStart())
async def start(message: Message, session: AsyncSession):
    if message.from_user is not None:
        await save_user_if_new(
            session=session,
            tg_user_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
        )
    await message.answer("Добро пожаловать! Откройте меню:", reply_markup=main_menu_kb())


