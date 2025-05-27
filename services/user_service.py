from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import UserGetSchemaAll


'''async def check_user(session: AsyncSession, model: type, field: str, value: str):
    existing_user = await session.execute(select(model).where(getattr(model, field) == value))
    if existing_user.scalar_one_or_none() is not None:
        raise HTTPException(status_code=404, detail="This email/telegram is already registered")'''


def get_all_users(email_users, telegram_users):
    all_users = []

    for user in email_users:
        all_users.append(UserGetSchemaAll(
            id=user.id,
            full_name=user.full_name,
            email=user.email,
            password=user.password
        ))

    for user in telegram_users:
        all_users.append(UserGetSchemaAll(
            id=user.id,
            full_name=user.full_name,
            telegram=user.telegram,
            password=user.password
        ))

    return all_users