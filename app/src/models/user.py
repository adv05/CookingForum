from typing import Optional
from sqlmodel import SQLModel, Field
from sqlalchemy import String
from sqlalchemy.sql.schema import Column


class UserBase(SQLModel):
    username: str
    email: str
    name: Optional[str]
    last_name: Optional[str]


class User_DB(UserBase, table=True):
    username: str = Field(sa_column=Column("username", String, unique=True))
    email: str = Field(sa_column=Column("email", String, unique=True))
    id: Optional[int] = Field(default=None, primary_key=True)
    password: str
    otp: str = None
    enabled_2FA: bool = False
    isAdmin: bool = False


class UserCreate(UserBase):
    password: str
    enabled_2FA: bool = False


class UserRead(UserBase):
    id: int
    enabled_2FA: bool
    isAdmin: bool
