from fastapi import FastAPI

from app.database import engine
from app.models import Base
from app.routers.datasets import router as datasets_router

app = FastAPI()

app.include_router(datasets_router)

Base.metadata.create_all(bind=engine)