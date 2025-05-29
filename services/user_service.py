from engine.session import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from models.user import UserGetSchemaAll, UserModelEmail, UserModelTelegram, UserSchemaEmail, UserSchemaTelegram
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def check_user(session: AsyncSession, model: type, field: str, value: str):
    existing_user = await session.execute(select(model).where(getattr(model, field) == value))
    if existing_user.scalar_one_or_none() is not None:
        raise HTTPException(status_code=400, detail="This email/telegram is already registered")


async def add_user_email(user: UserSchemaEmail, session: AsyncSession):
    await check_user(session, UserModelEmail, 'email', user.email)
    new_user = UserModelEmail(
        full_name = user.full_name,
        email = user.email,
        password = pwd_context.hash(user.password)
    )
    session.add(new_user)
    await session.commit()
    return user


async def add_user_telegram(user: UserSchemaTelegram, session: AsyncSession):
    await check_user(session, UserModelTelegram, 'telegram', user.telegram)
    new_user = UserModelTelegram(
        full_name = user.full_name,
        telegram = user.telegram,
        password = pwd_context.hash(user.password)
    )
    session.add(new_user)
    await session.commit()
    return user


async def get_all_users(email_users, telegram_users):
    all_users = []

    for user in email_users:
        all_users.append(UserGetSchemaAll(
            id=user.id,
            full_name=user.full_name,
            email=user.email,
            hashed_password=user.password
        ))

    for user in telegram_users:
        all_users.append(UserGetSchemaAll(
            id=user.id,
            full_name=user.full_name,
            telegram=user.telegram,
            hashed_password=user.password
        ))

    return all_users