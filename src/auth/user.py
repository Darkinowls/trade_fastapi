from typing import Optional

from fastapi_users import schemas, models
from pydantic import EmailStr


# YOU CAN USE BASE OR DICT MODEL

class UserRead(schemas.BaseUser[int]):
    role_id: int
    username: str

    id: models.ID
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserCreate(schemas.CreateUpdateDictModel):
    username: str

    email: EmailStr
    password: str
    # is_active: Optional[bool] = True
    # is_superuser: Optional[bool] = False
    # is_verified: Optional[bool] = False


# class UserUpdate(schemas.BaseUserUpdate):
#     role_id: Optional[int] = None
#     username: Optional[str] = None
#
#     password: Optional[str] = None
#     email: Optional[EmailStr] = None
#     is_active: Optional[bool] = None
#     is_superuser: Optional[bool] = None
#     is_verified: Optional[bool] = None
