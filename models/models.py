import asyncio

from sqlalchemy import Column, Integer
from sqlalchemy import MetaData
from sqlalchemy import select
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base

from config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME

meta_data = MetaData()
Base = declarative_base()

my_engine = create_async_engine(
    f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    echo=True,
)

class Roles(Base):
    __tablename__ = "roles"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer)
    city = Column(String)
    degree = Column(String, nullable=False, default="bachelor")
