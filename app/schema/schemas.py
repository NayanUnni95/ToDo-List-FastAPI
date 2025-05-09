from pydantic import BaseModel, UUID4
from typing import Optional


class UserSignup(BaseModel):
    name: str
    uname: str
    password: str


class SignupRes(BaseModel):
    id: Optional[UUID4]
    name: str
    uname: str
    message: str = "Success..."

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    uname: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str | None = "bearer"


class TokenData(BaseModel):
    username: str | None = None


class InvalidInput(BaseModel):
    status_code: int
    description: str | None = "Invalid"
