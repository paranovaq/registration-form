from fastapi import APIRouter
from api.services import users
from api.database.session import SessionDep
from api.schemas.users import(
    UserSchemaEmail,
    UserSchemaTelegram,
    UserGetSchemaEmail,
    UserGetSchemaTelegram,
    UserGetSchemaAll
)


router = APIRouter()


@router.post("/email", response_model=UserSchemaEmail)
async def add_user_email(user: UserSchemaEmail, session: SessionDep):
    return await users.add_user_email(user, session)


@router.post("/telegram", response_model=UserSchemaTelegram)
async def add_user_telegram(user: UserSchemaTelegram, session: SessionDep):
    return await users.add_user_telegram(user, session)


@router.get("/email/{email}", response_model=UserGetSchemaEmail)
async def get_user_email(email: str, session: SessionDep):
    return await users.get_user_email(email, session)


@router.get("/telegram/{telegram}", response_model=UserGetSchemaTelegram)
async def get_user_telegram(telegram: str, session: SessionDep):
    return await users.get_user_telegram(telegram, session)


@router.get("/email", response_model=list[UserGetSchemaEmail])
async def get_users_email(session: SessionDep):
    return await users.get_users_email(session)


@router.get("/telegram", response_model=list[UserGetSchemaTelegram])
async def get_users_telegram(session: SessionDep):
    return await users.get_users_telegram(session)


@router.get("/users", response_model=list[UserGetSchemaAll])
async def get_all_users(session: SessionDep):
    email_users = await get_users_email(session)
    telegram_users = await get_users_telegram(session)
    return await users.get_all_users(email_users, telegram_users)