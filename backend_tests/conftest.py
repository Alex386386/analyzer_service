import asyncio
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from dotenv import find_dotenv, load_dotenv
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from src.core.config import settings
from src.core.db import Base, get_async_session
from src.main import app

load_dotenv(find_dotenv())

DATABASE_URL_TEST = "sqlite+aiosqlite:///./test.db"

async_engine = create_async_engine(
    DATABASE_URL_TEST,
    connect_args={"check_same_thread": False},
    poolclass=NullPool,
)
TestingSessionLocal = async_sessionmaker(
    bind=async_engine, autocommit=False, autoflush=False, expire_on_commit=False
)

Base.metadata.bind = async_engine


async def override_get_async_session():
    async with TestingSessionLocal() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture
def get_test_headers():
    token = settings.access_token
    return {"Authorization": f"Bearer {token}"}


@pytest_asyncio.fixture(autouse=True, scope="session")
async def prepare_database():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
def set_test_mode():
    settings.test = True


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
