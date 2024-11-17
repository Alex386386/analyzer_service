from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from src.core.config import settings

# Sync DB connection for celery
sync_database_url = URL.create(
    drivername="postgresql+psycopg2",
    username=settings.postgres_user,
    password=settings.postgres_password,
    host=settings.db_host,
    port=settings.db_port,
    database=settings.db_name,
)

engine = create_engine(sync_database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Async DB connection
database_url = URL.create(
    drivername="postgresql+asyncpg",
    username=settings.postgres_user,
    password=settings.postgres_password,
    host=settings.db_host,
    port=settings.db_port,
    database=settings.db_name,
)

async_engine = create_async_engine(database_url, future=True)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine, autoflush=False, expire_on_commit=False, autocommit=False
)


async def get_async_session():
    async with AsyncSessionLocal() as async_session:
        yield async_session


class Base(DeclarativeBase):
    pass
