from pydantic import BaseModel, Field
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import Optional, Annotated


class Base(DeclarativeBase):
    pass


class UserModelEmail(Base):
    __tablename__ = "emailUsers"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]


class UserModelTelegram(Base):
    __tablename__ = "telegramUsers"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str]
    telegram: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]


class UserSchemaEmail(BaseModel):
    full_name: Annotated[str, Field (default= "your_full_name" , pattern="^[a-zA-Z ]+$", min_length=2, max_length=64)]
    email: Annotated[str, Field (default= "your_email" , pattern='^[a-zA-Z0-9]+[a-zA-Z0-9._-]+[a-zA-Z0-9._-]+[a-zA-Z0-9._-]+[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+$', max_length=31)]
    password: Annotated[str, Field (default= "your_password" , pattern="^[a-zA-Z0-9]+$", min_length=8, max_length=100)]


class UserSchemaTelegram(BaseModel):
    full_name: Annotated[str, Field (default= "your_full_name" , pattern="^[a-zA-Z ]+$", min_length=2, max_length=64)]
    telegram: Annotated[str, Field (default= "your_telegram" , pattern="^@+[a-zA-Z]+[a-zA-Z0-9_]+$", min_length=5, max_length=32)]
    password: Annotated[str, Field (default= "your_password" , pattern="^[a-zA-Z0-9]+$", min_length=8, max_length=100)]


class UserGetSchemaEmail(BaseModel):
    id: int
    full_name: str
    email: str



class UserGetSchemaTelegram(BaseModel):
    id: int
    full_name: str
    telegram: str



class UserGetSchemaAll(BaseModel):
    id: int
    full_name: str
    email: Optional[str] = None
    telegram: Optional[str] = None
