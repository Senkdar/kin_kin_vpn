from __future__ import annotations

import uuid
from decimal import Decimal
from typing import Optional

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


def _to_asyncpg_url(database_url: str) -> str:
    """Преобразует postgresql://... в postgresql+asyncpg://..."""

    if database_url.startswith("postgresql+asyncpg://"):
        return database_url
    # также поддержим короткую форму postgres://
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
        echo=False
    )

    session_factory = async_sessionmaker[AsyncSession](bind=engine, expire_on_commit=False)

    return engine, session_factory


class Base(DeclarativeBase):
    pass


class TelegramUser(Base):
    __tablename__ = "users"

    tg_user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    first_name: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    balance: Mapped[Decimal] = mapped_column(Numeric[Decimal](18, 2), nullable=False, server_default="0")
    created_at: Mapped[str] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class BalanceTransaction(Base):
    __tablename__ = "balance_transactions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.tg_user_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    kind: Mapped[str] = mapped_column(String(32), nullable=False)  # e.g. 'topup'
    status: Mapped[str] = mapped_column(String(32), nullable=False)  # 'pending'|'succeeded'|'canceled'
    amount: Mapped["Decimal"] = mapped_column(Numeric[Decimal](18, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(8), nullable=False, default="RUB")
    external_id: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    created_at: Mapped[str] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[str] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    __table_args__ = (
        CheckConstraint("amount > 0", name="chk_amount_positive"),
        CheckConstraint("status in ('pending','succeeded','canceled')", name="chk_status_valid"),
        CheckConstraint("kind in ('topup')", name="chk_kind_valid"),
    )


