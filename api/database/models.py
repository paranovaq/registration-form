from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


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

