import email
from typing import List, Optional

from pydantic import BaseModel


class User(BaseModel):
    email: str


class UserCreate(BaseModel):
    email: str
    password: str


class User_login(UserCreate):
    pass


class Token(BaseModel):
    token: str


class paper_name(BaseModel):
    owner_email: str
    title: str


class Paper(BaseModel):
    title: str
    description: str
    public: bool


class Paper_submit(Paper):
    owner_email: str
    id: str
