from api.database.session import AsyncSession
from sqlalchemy import select
from api.database.models import UserModelEmail, UserModelTelegram
from api.dao.users import check_user
from api.exceptions import same_email_user, same_telegram_user, null_email_user, null_telegram_user
from api.schemas.users import UserSchemaEmail, UserSchemaTelegram, UserGetSchemaTelegram, UserGetSchemaEmail, UserGetSchemaAll
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def add_user_email(user: UserSchemaEmail, session: AsyncSession):
    if await check_user(session, UserModelEmail, 'email', user.email):
        raise same_email_user
    new_user = UserModelEmail(
        full_name = user.full_name,
        email = user.email,
        password = pwd_context.hash(user.password)
    )
    session.add(new_user)
    await session.commit()
    return user


async def add_user_telegram(user: UserSchemaTelegram, session: AsyncSession):
    if await check_user(session, UserModelTelegram, 'telegram', user.telegram):
        raise same_telegram_user
    new_user = UserModelTelegram(
        full_name = user.full_name,
        telegram = user.telegram,
        password = pwd_context.hash(user.password)
    )
    session.add(new_user)
    await session.commit()
    return user


async def get_user_email(email: str, session: AsyncSession) -> UserGetSchemaEmail:
    query = select(UserModelEmail).where(UserModelEmail.email == email)
    result = await session.execute(query)
    user = result.scalar_one_or_none()
    if not user:
        raise null_email_user
    return UserGetSchemaEmail(
        id=user.id,
        full_name=user.full_name,
        email=user.email
    )


async def get_user_telegram(telegram: str, session: AsyncSession) -> UserGetSchemaTelegram:
    query = select(UserModelTelegram).where(UserModelTelegram.telegram == telegram)
    result = await session.execute(query)
    user = result.scalar_one_or_none()
    if not user:
        raise null_telegram_user
    return UserGetSchemaTelegram(
        id=user.id,
        full_name=user.full_name,
        telegram=user.telegram
    )


async def get_users_email(session:AsyncSession) -> list[UserGetSchemaEmail]:
    query = select(UserModelEmail)
    result = await session.execute(query)
    users_email = result.scalars().all()
    return [UserGetSchemaEmail(
        id=user.id,
        full_name=user.full_name,
        email=user.email
    ) for user in users_email]


async def get_users_telegram(session:AsyncSession) -> list[UserGetSchemaTelegram]:
    query = select(UserModelTelegram)
    result = await session.execute(query)
    users_telegram = result.scalars().all()
    return [UserGetSchemaTelegram(
        id=user.id,
        full_name=user.full_name,
        telegram=user.telegram,
    ) for user in users_telegram]


async def get_all_users(email_users, telegram_users):
    all_users = []

    for user in email_users:
        all_users.append(UserGetSchemaAll(
            id=user.id,
            full_name=user.full_name,
            email=user.email,
        ))

    for user in telegram_users:
        all_users.append(UserGetSchemaAll(
            id=user.id,
            full_name=user.full_name,
            telegram=user.telegram,
        ))

    return all_users