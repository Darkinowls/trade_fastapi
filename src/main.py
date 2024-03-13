from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from starlette import status

from src.auth.router import auth_router

app = FastAPI(default_response_class=ORJSONResponse, debug=True, title="TEST")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(exc: RequestValidationError):
    return ORJSONResponse(
        content=exc.errors(),
        status_code=status.HTTP_400_BAD_REQUEST,
    )


app.include_router(
    auth_router
)
