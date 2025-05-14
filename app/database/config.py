"""
This module configures the database connection for a FastAPI application using SQLModel.
"""

from fastapi import Depends
from sqlmodel import create_engine, Session
from typing import Annotated
from decouple import config

POSTGRES_DB: str = config("POSTGRES_DB", default="sample")
POSTGRES_USER: str = config("POSTGRES_USER", default="postgres")
POSTGRES_HOST: str = config("POSTGRES_HOST", default="localhost")
POSTGRES_PORT: str = config("POSTGRES_PORT", default="5432")
POSTGRES_PASSWORD: str = config("POSTGRES_PASSWORD", default="postgres")
POSTGRES_DB_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

try:
    engine = create_engine(POSTGRES_DB_URL)
    with engine.connect() as connection:
        print("Successfully connected to the database!")
except Exception as e:
    print(f"Database connection error: {e}")


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
