import uuid
from typing import Optional
from pydantic import BaseModel, constr

from enum import Enum


class UserBase(BaseModel):
    id: Optional[uuid.UUID] = None
    fb_uid: Optional[str] = None
    name: Optional[str] = None
    password: Optional[str] = None
    age: Optional[int] = None
    email: Optional[str] = None
    avatar: Optional[str] = None
    browser_token: Optional[str] = None
    providers: Optional[str] = None
    fb_uid: Optional[str] = None
    is_verified: Optional[bool] = False
    client_browser: Optional[str] = None
    client_country: Optional[str] = None
    client_ip: Optional[str] = None
    is_deleted: Optional[bool] = False

    # class Config:
    #     orm_mode = True


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class FreeUserLogin(BaseModel):
    browser_token: constr(min_length=8)
    client_country: Optional[str]
    client_ip: Optional[str]


class SessionLoginInput(BaseModel):
    id_token: str


class SignInWithEnum(str, Enum):
    google = "google.com"
    apple = "apple.com"


class OutputSessionLogin(BaseModel):
    id: str
    email: str
    token: str = "token"


class OutputUser(UserBase):
    total_likes: Optional[int]
