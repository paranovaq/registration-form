from api.database.session import AsyncSession
from sqlalchemy import select


async def check_user(session: AsyncSession, model: type, field: str, value: str):
    existing_user = await session.execute(select(model).where(getattr(model, field) == value))
    return existing_user.scalar_one_or_none() is not None