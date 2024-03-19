from redis import asyncio as aioredis
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from starlette import status
from starlette.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from src.auth.router import auth_router
from src.chat.router import chat_router
from src.operations.router import op_r
from src.pages.router import page_router
from src.tasks.router import task_router

app = FastAPI(default_response_class=ORJSONResponse, debug=True, title="TEST")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return ORJSONResponse(
        content=exc.errors()[0].get('msg', None),
        status_code=status.HTTP_400_BAD_REQUEST,
    )


app.include_router(
    auth_router,
)
app.include_router(
    op_r,
)
app.include_router(
    task_router,
)
app.include_router(
    page_router,
)
app.include_router(
    chat_router,
)

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # COOKIE
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    # SOMETIMES WE HAVE ERRORS. PUT YOUR HEADERS HERE
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    # just redis
    redis = aioredis.from_url("redis://localhost:6379")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


app.mount("/static", StaticFiles(directory="src/static"), name="static")
