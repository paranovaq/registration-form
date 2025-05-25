from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: str


settings = Config()

from typing import Annotated, Optional
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


app = FastAPI()


engine = create_async_engine(
    f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@"
    f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}",
    echo=True
)

new_async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with new_async_session() as session:
        yield session

async def check_user(session: AsyncSession ,model: type, field: str, value: str):
    existing_user = await session.execute(select(model).where(getattr(model, field) == value))
    if existing_user.scalar_one_or_none() is not None:
        raise HTTPException(status_code=404, detail="This email/telegram is already registered")



SessionDep = Annotated[AsyncSession, Depends(get_session)]


class Base(DeclarativeBase):
    pass


class UserModelEmail(Base):
    __tablename__ = "emailUsers"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]


class UserModelTelegram(Base):
    __tablename__ = "telegramUsers"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str]
    telegram: Mapped[str]
    password: Mapped[str]


class UserSchemaEmail(BaseModel):
    full_name: str
    email: str
    password: str


class UserSchemaTelegram(BaseModel):
    full_name: str
    telegram: str
    password: str


class UserGetSchemaEmail(BaseModel):
    id: int
    full_name: str
    email: str
    password: str


class UserGetSchemaTelegram(BaseModel):
    id: int
    full_name: str
    telegram: str
    password: str


class UserGetSchemaAll(BaseModel):
    id: int
    full_name: str
    email: Optional[str] = None
    telegram: Optional[str] = None
    password: str



@app.post("/setup")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        return {"ok": True}


@app.post("/users/email")
async def add_user_email(user: UserSchemaEmail, session: SessionDep) -> UserSchemaEmail:
    await check_user (session, UserModelEmail, "email", user.email)
    new_user = UserModelEmail(
        full_name=user.full_name,
        email=user.email,
        password=user.password,
    )
    session.add(new_user)
    await session.commit()
    return user


@app.post("/users/telegram")
async def add_user_telegram(user: UserSchemaTelegram, session: SessionDep) -> UserSchemaTelegram:
    await check_user (session, UserModelTelegram, "telegram", user.telegram)
    new_user = UserModelTelegram(
        full_name=user.full_name,
        telegram=user.telegram,
        password=user.password,
    )
    session.add(new_user)
    await session.commit()
    return user


@app.get("/users/email")
async def get_users_email(session: SessionDep) -> list[UserGetSchemaEmail]:
    query = select(UserModelEmail)
    result = await session.execute(query)
    users_email = result.scalars().all()
    return [UserGetSchemaEmail(id=user.id, full_name=user.full_name, email=user.email,  password = user.password) for user in users_email]


@app.get("/users/telegram")
async def get_users_telegram(session: SessionDep) -> list[UserGetSchemaTelegram]:
    query = select(UserModelTelegram)
    result = await session.execute(query)
    users_telegram = result.scalars().all()
    return [UserGetSchemaTelegram(id=user.id, full_name=user.full_name, telegram=user.telegram,  password = user.password) for user in users_telegram]


@app.get("/users")
async def get_all_users(session: SessionDep) -> list[UserGetSchemaAll]:
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