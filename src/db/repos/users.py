from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert as pg_insert

from db.models import TelegramUser


async def upsert_user(
    session: AsyncSession,
    tg_user_id: int,
    username: Optional[str],
    first_name: Optional[str],
    last_name: Optional[str],
) -> None:
    stmt = (
        pg_insert(TelegramUser)
        .values(
            tg_user_id=tg_user_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        .on_conflict_do_nothing(index_elements=["tg_user_id"])
    )
    await session.execute(stmt)
    await session.commit()




