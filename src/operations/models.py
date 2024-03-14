from datetime import datetime

from sqlalchemy import Integer, TIMESTAMP, String, Column, MetaData
from sqlalchemy.orm import mapped_column

from src.database import Base

meta_data = Base.metadata


class Operation(Base):
    __tablename__ = "operation"
    id = Column(Integer, primary_key=True)
    quantity = mapped_column(Integer, nullable=False)
    figi = mapped_column(String, nullable=False)
    instrument_type = mapped_column(String, nullable=False)
    date = mapped_column(TIMESTAMP, default=datetime.now(), nullable=False)
    type = mapped_column(String, nullable=False)
