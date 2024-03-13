from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

meta_data = MetaData()
Base = declarative_base()


class Role(Base):
    __tablename__ = "role"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String, nullable=False)


class User(SQLAlchemyBaseUserTable, Base):
    __tablename__ = "user"

    username = mapped_column(String, nullable=False)
    id = mapped_column(Integer, primary_key=True)
    role_id = mapped_column(Integer, ForeignKey("role.id"))
    email = mapped_column(String(length=320), unique=True, index=False, nullable=True)
    # email: Mapped[str] = mapped_column(
    #     String(length=320), unique=True, index=True, nullable=False
    # )
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
