from enum import Enum
from enum import Enum
from typing import List, Optional

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel, Field, ValidationError
from starlette import status

from models.models import my_engine

app = FastAPI(default_response_class=ORJSONResponse, debug=True, title="TEST")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    return ORJSONResponse(
        content=exc.errors(),
        status_code=status.HTTP_400_BAD_REQUEST,
    )


data = [
    {"name": "John", "age": 31, "city": "New York"},
    {"name": "sdadas", "age": 31, "city": "New York"},
    {"name": "John", "age": 31, "city": "New York"},
    {"name": "John", "age": 31, "city": "New York"},
    {"name": "John", "age": 31, "city": "New York"},
    {"name": "John", "age": 31, "city": "New York"},
    {"name": "John", "age": 31, "city": "New York"},
    {"name": "John", "age": 31, "city": "New York"},
    {"name": "John", "age": 31, "city": "New York"},
    {"name": "John", "age": 31, "city": "New York"},
    {"name": "John", "age": 32, "city": "New York"},
    {"name": "John", "age": 32, "city": "New York"},
    {"name": "John", "age": 32, "city": "New York"},
    {"name": "John", "age": 32, "city": "New York"},
    {"name": "John", "age": 32, "city": "New York"},
    {"name": "John", "age": 32, "city": "New York"},
    {"name": "John", "age": 32, "city": "New York"},
    {"name": "John", "age": 32, "city": "New York"},
    {"name": "John", "age": 32, "city": "New York"},
    {"name": "John", "age": 32, "city": "New York"},
    {"name": "John", "age": 33, "city": "New York"},
    {"name": "John", "age": 33, "city": "New York"},
    {"name": "John", "age": 33, "city": "New York"},
    {"name": "John", "age": 33, "city": "New York"},
    {"name": "John", "age": 33, "city": "New York"},
    {"name": "John", "age": 33, "city": "New York"},
    {"name": "John", "age": 33, "city": "New York"},
    {"name": "John", "age": 33, "city": "New York"},
    {"name": "John", "age": 33, "city": "New York"},
    {"name": "John", "age": 33, "city": "New York"},
    {"name": "John", "age": 34, "city": "New York"},
    {"name": "John", "age": 34, "city": "New York"},
    {"name": "John", "age": 34, "city": "New York"},
    {"name": "John", "age": 34, "city": "New York"},
    {"name": "John", "age": 34, "city": "New York"},
    {"name": "John", "age": 34, "city": "New York"},
]


class Degree(Enum):
    bachelor = "bachelor"
    master = "master"
    doctor = "doctor"


class UserSchema(BaseModel):
    name: str
    age: int
    city: str


class TradeSchema(BaseModel):
    name: str = None
    age: int = Field(ge=0, le=1000)
    city: str
    user: UserSchema
    degree: Optional[Degree]


@app.post("/users")
async def create_user(trade: TradeSchema) -> List[TradeSchema]:
    trade.age = 'ads'
    return [trade]


