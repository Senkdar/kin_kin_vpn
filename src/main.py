import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from db.models import init_db
from middlewares.db_session import DbSessionMiddleware
from bot.routers.menu import menu_router
from bot.routers.start import start_router

load_dotenv()

bot_token = os.getenv("BOT_TOKEN")
if not bot_token:
    raise RuntimeError("BOT_TOKEN не задан. Укажите в .env или переменных окружения.")

bot = Bot(token=bot_token)
dp = Dispatcher()

ENGINE: AsyncEngine | None = None
SESSION_FACTORY: async_sessionmaker[AsyncSession] | None = None

async def main():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL не задан.")
    engine = None

    engine, session_factory = await init_db(database_url)
    dp.update.middleware(DbSessionMiddleware(session_factory))

    # Роутеры
    dp.include_router(start_router)
    dp.include_router(menu_router)

    try:
        await dp.start_polling(bot)
    finally:
        if engine is not None:
            await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
