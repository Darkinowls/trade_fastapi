from typing import Union

from fastapi import APIRouter, Depends, HTTPException
from fastapi_users import FastAPIUsers
from sqlalchemy import select, Result, CursorResult, Row
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from src.auth.auth import auth_backend
from src.auth.models import User, Role
from src.auth.user import UserRead, UserCreate
from src.auth.user_manager import get_user_manager
from src.database import get_async_session

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

auth_router = APIRouter(
    prefix="/auth/jwt",
    tags=["auth"],
)

auth_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
)

auth_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
)

current_user = fastapi_users.current_user()


async def get_role_by_user(user, session: AsyncSession) -> Row:
    state = select(Role.name, Role.id).where(Role.id == user.role_id)
    result: Union[Result, CursorResult] = await session.execute(state)
    row: Row = result.scalars().first()
    return row


@auth_router.get("/protected-route")
async def protected_route(user: User = Depends(current_user),
                          session: AsyncSession = Depends(get_async_session)) -> str:
    row: Row = await get_role_by_user(user, session)

    return f"Hello, {row}!"


class AuthGuard:
    __slots__ = ("token",)

    def __init__(self, token: str):
        self.token = token

    async def __call__(self, request: Request):
        # print(repr(self.token))
        if request.cookies.get("token", None) != self.token:
            raise HTTPException(status_code=401, detail="Token is error")


auth_payment = AuthGuard("e")

# new_api_router = APIRouter(
#     prefix="/new_api_router",
#     tags=["new_api_router"],
#     Can be OVERRIDED by dependencies
#     dependencies=[Depends(auth_payment)],
# )

@auth_router.get("/auth", dependencies=[Depends(auth_payment)])
async def auth() -> str:
    return "Hello, row!"
