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
