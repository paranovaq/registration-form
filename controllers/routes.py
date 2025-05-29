from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from services import user_service
from psycopg2 import IntegrityError
from engine.session import SessionDep, engine
from passlib.context import CryptContext
from models.user import(
    Base,
    UserModelEmail,
    UserModelTelegram,
    UserSchemaEmail,
    UserSchemaTelegram,
    UserGetSchemaEmail,
    UserGetSchemaTelegram,
    UserGetSchemaAll
)


router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/setup")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        return {"ok": True}


@router.post("/email", response_model=UserSchemaEmail)
async def add_user_email(user: UserSchemaEmail, session: SessionDep):
    new_user = UserModelEmail(
        full_name = user.full_name,
        email = user.email,
        password = pwd_context.hash(user.password)
    )
    session.add(new_user)
    await session.commit()
    return user
'''try:
        await session.commit()
    except IntegrityError:
            await session.rollback()
            raise HTTPException(
                    status_code=400,
                    detail="Email already registered")
    return user'''



@router.post("/telegram", response_model=UserSchemaTelegram)
async def add_user_telegram(user: UserSchemaTelegram, session: SessionDep):
    new_user = UserModelTelegram(
        full_name=user.full_name,
        telegram=user.telegram,
        password=pwd_context.hash(user.password),
    )
    session.add(new_user)
    await session.commit()
    return user
'''try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
                status_code=400,
                detail="Email already registered")
    return user'''


@router.get("/email", response_model=list[UserGetSchemaEmail])
async def get_users_email(session: SessionDep):
    query = select(UserModelEmail)
    result = await session.execute(query)
    users_email = result.scalars().all()
    return [UserGetSchemaEmail(
        id=user.id,
        full_name=user.full_name,
        email=user.email,
        hashed_password=user.password
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
        hashed_password=user.password
    ) for user in users_telegram]


@router.get("/users", response_model=list[UserGetSchemaAll])
async def get_all_users(session: SessionDep):
    email_users = await get_users_email(session)
    telegram_users = await get_users_telegram(session)
    return user_service.get_all_users(email_users, telegram_users)