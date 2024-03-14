from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from pydantic import Field
from pydantic.main import BaseModel
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.operations.models import Operation
from src.operations.schema import OperationCreateRequest

op_r = APIRouter(
    prefix="/operations",
    tags=["Operation"],
)


@op_r.get("/")
async def get_operations(bigger_than: int = Query(ge=0), session: AsyncSession = Depends(get_async_session)):
    q = select(Operation).where(Operation.id > bigger_than)  # type: ignore
    r = await session.execute(q)
    return {"message": r.scalars().all()}


@op_r.post("/")
async def add_operation(operation: OperationCreateRequest, session: AsyncSession = Depends(get_async_session)):

    # new style
    # op = Operation(**operation.dict())
    # session.add(op)
    # r = await session.commit()

    # old
    st = insert(Operation).values(**operation.dict())
    r = await session.execute(st)
    await session.commit()
    return {"message": r.returns_rows}
