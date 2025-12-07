from __future__ import annotations

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


def _to_asyncpg_url(database_url: str) -> str:
    """Преобразует postgresql://... в postgresql+asyncpg://..."""
    if database_url.startswith("postgresql+asyncpg://"):
        return database_url
    if database_url.startswith("postgres://"):
        return "postgresql+asyncpg://" + database_url[len("postgres://") :]
    if database_url.startswith("postgresql://"):
        return "postgresql+asyncpg://" + database_url[len("postgresql://") :]
    return database_url


async def init_db(database_url: str) -> tuple[AsyncEngine, async_sessionmaker[AsyncSession]]:
    async_url = _to_asyncpg_url(database_url)
    engine = create_async_engine(
        async_url,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
        echo=False,
    )
    session_factory = async_sessionmaker[AsyncSession](bind=engine, expire_on_commit=False)
    return engine, session_factory


