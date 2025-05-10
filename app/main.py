from fastapi import FastAPI
from .routers import user, todo
from .database.config import engine, Base

app = FastAPI()

app.include_router(user.router)
app.include_router(todo.router)

Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return "Connection successfully established to the server..."
