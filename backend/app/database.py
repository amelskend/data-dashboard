# database.py

import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

DATABASE_URL = (
    f"postgresql://"
    f"{os.getenv('POSTGRES_USER')}:"
    f"{os.getenv('POSTGRES_PASSWORD')}@"
    f"{os.getenv("DB_HOST")}:5432/"
    f"{os.getenv('POSTGRES_DB')}"
)

print("POSTGRES_USER =", os.getenv("POSTGRES_USER"))
print("POSTGRES_DB =", os.getenv("POSTGRES_DB"))
print("DB_HOST =", os.getenv("DB_HOST"))

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