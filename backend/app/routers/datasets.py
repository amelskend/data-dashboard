# routers/datasets.py
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from botocore.exceptions import BotoCoreError, ClientError

from app.models import Dataset
from app.schemas import DatasetCreate
from app.database import get_db
from app.storage import S3_BUCKET, s3

import pandas as pd

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

@router.post("/upload")
async def upload_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="A filename is required")

    try:
        # Pandas reads and analyzes the CSV before it becomes a Dataset.
        df = pd.read_csv(file.file)
        df = df.dropna(how="all")
        df.columns = df.columns.str.strip()

        file.file.seek(0)
        s3.upload_fileobj(file.file, S3_BUCKET, file.filename)

        dataset_name = file.filename.rsplit(".", 1)[0]
        new_dataset = Dataset(name=dataset_name, rows=len(df))
        db.add(new_dataset)
        db.commit()
        db.refresh(new_dataset)
    except (pd.errors.EmptyDataError, pd.errors.ParserError) as error:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is not a valid CSV",
        ) from error
    except (BotoCoreError, ClientError, ValueError) as error:
        raise HTTPException(
            status_code=503,
            detail="Object storage is unavailable or the CSV is invalid",
        ) from error
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=503,
            detail="The dataset could not be saved to PostgreSQL",
        ) from error

    return {
        "rows": len(df),
        "columns": list(df.columns),
        "dataset": {
            "id": new_dataset.id,
            "name": new_dataset.name,
            "rows": new_dataset.rows,
        },
    }