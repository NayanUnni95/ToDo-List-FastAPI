from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config

POSTGRES_DB: str = config("POSTGRES_DB", default="sample")
POSTGRES_USER: str = config("POSTGRES_USER", default="postgres")
POSTGRES_HOST: str = config("POSTGRES_HOST", default="localhost")
POSTGRES_PORT: str = config("POSTGRES_PORT", default="5432")
POSTGRES_PASSWORD: str = config("POSTGRES_PASSWORD", default="postgres")
POSTGRES_DB_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

try:
    engine = create_engine(POSTGRES_DB_URL)
    session = sessionmaker(bind=engine, autoflush=False)
    Base = declarative_base()
    with engine.connect() as connection:
        print("Successfully connected to the database!")
except Exception as e:
    print(f"Database connection error: {e}")


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()
