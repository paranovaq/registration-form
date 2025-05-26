from models.user import Base
from engine.session import engine
from fastapi import APIRouter
from sqlalchemy import select
'''from services.user_service import check_user'''
from engine.session import SessionDep
from models.user import(
    UserModelEmail,
    UserModelTelegram,
    UserSchemaEmail,
    UserSchemaTelegram,
    UserGetSchemaEmail,
    UserGetSchemaTelegram,
    UserGetSchemaAll
)

router = APIRouter()


@router.post("/setup")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        return {"ok": True}
@router.post("/email", response_model=UserSchemaEmail)
async def add_user_email(user: UserSchemaEmail, session: SessionDep):
    '''await check_user(session, UserModelEmail, "email", user.email)'''
    new_user = UserModelEmail(
        full_name=user.full_name,
        email=user.email,
        password=user.password,
    )
    session.add(new_user)
    await session.commit()
    return user


@router.post("/telegram", response_model=UserSchemaTelegram)
async def add_user_telegram(user: UserSchemaTelegram, session: SessionDep):
    '''await check_user(session, UserModelTelegram, "telegram", user.telegram)'''
    new_user = UserModelTelegram(
        full_name=user.full_name,
        telegram=user.telegram,
        password=user.password,
    )
    session.add(new_user)
    await session.commit()
    return user


@router.get("/email", response_model=list[UserGetSchemaEmail])
async def get_users_email(session: SessionDep):
    query = select(UserModelEmail)
    result = await session.execute(query)
    users_email = result.scalars().all()
    return [UserGetSchemaEmail(
        id=user.id,
        full_name=user.full_name,
        email=user.email,
        password=user.password
    ) for user in users_email]


@router.get("/telegram", response_model=list[UserGetSchemaTelegram])
async def get_users_telegram(session: SessionDep):
    query = select(UserModelTelegram)
    result = await session.execute(query)
    users_telegram = result.scalars().all()
    return [UserGetSchemaTelegram(
        id=user.id,
        full_name=user.full_name,
        telegram=user.telegram,
        password=user.password
    ) for user in users_telegram]


@router.get("/users", response_model=list[UserGetSchemaAll])
async def get_all_users(session: SessionDep):
    email_users = await get_users_email(session)
    telegram_users = await get_users_telegram(session)
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