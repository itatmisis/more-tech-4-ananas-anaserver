from asyncio import current_task
import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv(".env", override=True)

user = os.getenv("USER")
password = os.getenv("PASSWORD")
host = os.getenv("HOST")
db = os.getenv("DB")


DATABASE_URL = f"postgresql+asyncpg://{user}:{password}@{host}:54320/{db}"
# DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base()
async_session_factory = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
async_scoped_session_factory = async_scoped_session(async_session_factory, scopefunc=current_task)


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    session = async_scoped_session_factory()
    await session.execute("CREATE EXTENSION IF NOT EXISTS vector")


# Dependency
async def get_session():
    async with async_scoped_session_factory() as session:  # type: ignore
        yield session
