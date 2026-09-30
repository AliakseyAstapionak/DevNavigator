import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import AsyncGenerator
from sqlalchemy.orm import DeclarativeBase
load_dotenv()

import os


DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")

DB_URL = os.getenv("DATABASE_URL")
if DB_URL:
    DB_URL = DB_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
else:
    DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}" 

engine = create_async_engine(DB_URL, echo=False, pool_size=20, max_overflow=20, pool_timeout=30)
async_session_maker = async_sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False 
    )

class Base(DeclarativeBase):
    pass

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session