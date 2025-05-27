from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import Optional




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
    telegram: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str]


class UserSchemaEmail(BaseModel):
    full_name: str
    email: EmailStr
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