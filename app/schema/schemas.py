from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import datetime


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


class CurrentUser(BaseException):
    id: Optional[UUID4]
    name: str
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


class TodoBase(BaseModel):
    title: str
    desc: str
    deadline: datetime


class CreateTodo(TodoBase):
    pass


class EditTodo(TodoBase):
    taskId: int
    isCompleted: bool


class ShowAllTodo(BaseModel):
    taskId: int
    title: str
    desc: str
    deadline: str
    isCompleted: str
