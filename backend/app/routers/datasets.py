# routers/datasets.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.models import Dataset
from app.schemas import DatasetCreate
from app.database import get_db

router = APIRouter()

@router.post("/datasets")
def create_dataset(
    dataset: DatasetCreate,
    db: Session = Depends(get_db)
):

    new_dataset = Dataset(
        name=dataset.name,
        rows=dataset.rows
    )

    db.add(new_dataset)

    db.commit()

    db.refresh(new_dataset)

    return new_dataset

@router.get("/datasets")
def get_datasets(db: Session = Depends(get_db)):

    datasets = db.query(Dataset).all()

    return datasets

@router.get("/datasets/{dataset_id}")
def get_dataset(
    dataset_id: int,
    db: Session = Depends(get_db)
):

    dataset = (
        db.query(Dataset)
        .filter(Dataset.id == dataset_id)
        .first()
    )

    if not dataset:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found"
        )

    return dataset

@router.delete("/datasets/{dataset_id}")
def delete_dataset(
    dataset_id: int,
    db: Session = Depends(get_db)
):

    dataset = (
        db.query(Dataset)
        .filter(Dataset.id == dataset_id)
        .first()
    )

    if not dataset:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found"
        )

    db.delete(dataset)

    db.commit()

    return {
        "message": "Dataset deleted"
    }
