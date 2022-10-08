import os

from dotenv import find_dotenv, load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv(find_dotenv())

user = os.getenv("USER")
password = os.getenv("PASSWORD")
host = os.getenv("HOST")
db = os.getenv("DB")


DATABASE_URL = f"postgresql://{user}:{password}@{host}/{db}"
# DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base()
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Dependency
async def get_session() -> AsyncSession:  # type: ignore
    async with async_session() as session:  # type: ignore
        yield session
