from pathlib import Path

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from starlette.responses import HTMLResponse

from src.operations.router import get_operations
from src.util import Res

page_router = APIRouter(
    prefix="/pages",
    tags=["Pages"],
)

template = Jinja2Templates(directory='src/templates')


@page_router.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    return template.TemplateResponse(
        request=request,
        name="base.html")


@page_router.get("/search", response_class=HTMLResponse)
async def get_index(request: Request, operations: Res=Depends(get_operations)):
    # select(Operation)

    return template.TemplateResponse(
        request=request,
        name="search.html",
        context={"operations": operations.message}
    )

@page_router.get("/chat", response_class=HTMLResponse)
async def get_index(request: Request):
    # select(Operation)

    return template.TemplateResponse(
        request=request,
        name="chat.html",
    )
