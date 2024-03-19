import asyncio
from typing import AsyncGenerator

from starlette.testclient import TestClient

from src.database import get_async_session
from src.main import app
import pytest
from httpx import AsyncClient
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.auth.models import meta_data
from src.config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME

TEST_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}_test"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    poolclass=NullPool
)

_async_session_maker = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)

meta_data.bind = test_engine


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with _async_session_maker() as session:
        yield session


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(meta_data.create_all)
    # Test will run
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(meta_data.drop_all)


# SETUP
@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


app.dependency_overrides[get_async_session] = override_get_async_session

client = TestClient(app)

@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
