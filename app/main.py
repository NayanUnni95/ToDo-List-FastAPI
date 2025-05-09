from fastapi import FastAPI
from .routers import user
from .database.config import engine, Base
from .model import models

app = FastAPI()
app.include_router(user.router)


Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return "Connection successfully established to the server..."
