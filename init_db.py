import asyncio
from app.core.database import Base, engine
from app.models.client import Client
from app.models.project import Project
from app.models.activity import Activity


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print("Database initialized successfully!")


if __name__ == "__main__":
    asyncio.run(init_db())
