from typing import AsyncIterator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from core.config import settings

class Base(DeclarativeBase):
    pass

engine = create_async_engine(
    str(settings.DATABASE_URL), 
    echo=True, # TODO: Útil en desarrollo para ver las queries en consola
    future=True
)

async_session_generator = async_sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False,
    autoflush=False
)

async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all) # TODO: solo en desarrollo

async def get_async_session() -> AsyncIterator[AsyncSession]:
    async with async_session_generator() as session:
        yield session