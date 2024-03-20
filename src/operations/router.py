import asyncio
from time import sleep

from fastapi import APIRouter, Depends, Query
from fastapi_cache.decorator import cache
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.operations.models import Operation
from src.operations.schema import OperationCreateRequest
from src.util import Res

op_r = APIRouter(
    prefix="/operations",
    tags=["Operation"],
)


@op_r.get("/")
async def get_operations(bigger_than: int = Query(0, ge=0), session: AsyncSession = Depends(get_async_session)):
    q = select(Operation).limit(2).where(Operation.id > bigger_than)  # type: ignore
    r = await session.execute(q)
    # raise HTTPException(status_code=401, detail="Operation created?")
    return Res(r.scalars().all())


class OffsetLimit:
    """
    This is a class for OffsetLimit.
    Це інший спосіб використання Depends замість просто функції
    """
    def __init__(self, offset: int = 0, limit: int = 10):
        self.offset = offset
        self.limit = limit


# @op_r.get("/paginate")
# async def paginate(offset: int = 0, limit: int = 10):
#     return OffsetLimit(offset, limit)


@op_r.get("/get_operations2")
async def get_operations2(ol: OffsetLimit = Depends(), session=Depends(get_async_session)):
    q = select(Operation).limit(ol.limit).offset(ol.offset)
    r = await session.execute(q)
    return Res(r.scalars().all())


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
    return Res(r.returns_rows)


@op_r.get("/long")
@cache(expire=100)
async def long_operation():
    sleep(2)
    return Res('good')
