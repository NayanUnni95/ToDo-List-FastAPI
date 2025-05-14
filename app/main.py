from fastapi import FastAPI
from sqlmodel import SQLModel

from .routers import user
from .database.config import engine
from .model.models import Users, Tasks

app = FastAPI()

app.include_router(user.router)
# app.include_router(todo.router)


SQLModel.metadata.create_all(engine)


@app.get("/")
def root():
    return "Connection successfully established to the server..."
