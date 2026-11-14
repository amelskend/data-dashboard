# models.py

from sqlalchemy import Column, Integer, String


from app.database import Base


class Dataset(Base):

    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True)

    name = Column(String)

    rows = Column(Integer)