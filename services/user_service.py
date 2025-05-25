from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def check_user(session: AsyncSession, model: type, field: str, value: str):
    existing_user = await session.execute(select(model).where(getattr(model, field) == value))
    if existing_user.scalar_one_or_none() is not None:
        raise HTTPException(status_code=404, detail="This email/telegram is already registered")