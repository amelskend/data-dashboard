from fastapi import FastAPI

from app.database import engine
from app.models import Base, Dataset
from app.schemas import DatasetCreate
from app.database import SessionLocal

app = FastAPI()

@app.post("/datasets")
def create_dataset(dataset: DatasetCreate):

    db = SessionLocal()

    new_dataset = Dataset(
        name=dataset.name,
        rows=dataset.rows
    )

    db.add(new_dataset)

    db.commit()

    db.refresh(new_dataset)

    return new_dataset

Base.metadata.create_all(bind=engine)