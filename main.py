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

from typing import Annotated
from fastapi import Depends, FastAPI
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


SessionDep = Annotated[AsyncSession, Depends(get_session)]


class Base(DeclarativeBase):
    pass


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str]
    email_or_tg: Mapped[str]
    password: Mapped[str]


class UserSchema(BaseModel):
    full_name: str
    email_or_tg: str
    password: str


class UserGetSchema(BaseModel):
    id: int
    full_name: str
    email_or_tg: str
    password: str


@app.post("/setup")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        return {"ok": True}


@app.post("/users")
async def add_user(user: UserSchema, session: SessionDep) -> UserSchema:
    new_user = UserModel(
    full_name = user.full_name,
    email_or_tg = user.email_or_tg,
    password = user.password,
    )
    session.add(new_user)
    await session.commit()
    return user


@app.get("/users")
async def get_users(session: SessionDep) -> list[UserGetSchema]:
    query = select(UserModel)
    result = await session.execute(query)
    users = result.scalars().all()
    return [UserGetSchema(id=user.id, full_name=user.full_name, email_or_tg=user.email_or_tg,  password = user.password) for user in users]