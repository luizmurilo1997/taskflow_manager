from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URL,
    echo=True,
    future=True
)

async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()


async def get_db():
    """
    Dependency generator for database sessions.
    Ensures proper handling of async database connections.

    Yields:
        AsyncSession: Database session for handling database operations
    """
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
