from datetime import datetime

from sqlalchemy import Integer, String, TIMESTAMP
from sqlalchemy.orm import mapped_column

from src.database import Base

meta_data = Base.metadata


class Message(Base):
    __tablename__ = "message"

    id = mapped_column(Integer, primary_key=True)
    text = mapped_column(String, nullable=False)
