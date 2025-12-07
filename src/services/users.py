from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from db.repos.users import upsert_user


async def save_user_if_new(
    session: AsyncSession,
    tg_user_id: int,
    username: Optional[str],
    first_name: Optional[str],
    last_name: Optional[str],
) -> None:
    await upsert_user(
        session,
        tg_user_id=tg_user_id,
        username=username,
        first_name=first_name,
        last_name=last_name,
    )


