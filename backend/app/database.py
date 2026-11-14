# database.py

import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

def _resolve_database_url():

    database_url = os.getenv("DATABASE_URL")

    if database_url:
        return database_url

    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    db = os.getenv("POSTGRES_DB")
    host = os.getenv("DB_HOST")

    if user and password and db and host:
        return (
            f"postgresql://"
            f"{user}:{password}@"
            f"{host}:5432/"
            f"{db}"
        )

    return "sqlite:///./app.db"

DATABASE_URL = _resolve_database_url()

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

Base = declarative_base()