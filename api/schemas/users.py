from pydantic import BaseModel, Field
from typing import Optional, Annotated
from api.schemas.regex import full_name_val, email_val, telegram_val, password_val


class UserSchemaEmail(BaseModel):
    full_name: Annotated[str, Field (default= "your_full_name", pattern=full_name_val, min_length=2, max_length=64)]
    email: Annotated[str, Field (default= "your_email", pattern=email_val, max_length=31)]
    password: Annotated[str, Field (default= "your_password", pattern=password_val, min_length=8, max_length=100)]


class UserSchemaTelegram(BaseModel):
    full_name: Annotated[str, Field (default= "your_full_name", pattern=full_name_val, min_length=2, max_length=64)]
    telegram: Annotated[str, Field (default= "your_telegram", pattern=telegram_val, min_length=5, max_length=32)]
    password: Annotated[str, Field (default= "your_password", pattern=password_val, min_length=8, max_length=100)]


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