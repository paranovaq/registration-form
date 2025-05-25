from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from settings.config import settings
from fastapi import Depends
from typing import Annotated

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