from pydantic import BaseModel


class DatasetCreate(BaseModel):
    name: str
    rows: int
    