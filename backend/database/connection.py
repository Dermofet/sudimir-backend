from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from sqlalchemy.schema import DropTable

from backend.config import config

engine = create_async_engine(
    config.DB_DSN.unicode_string(),
    echo=config.DEBUG,
)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
