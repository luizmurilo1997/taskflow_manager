import asyncio
from sqlalchemy import text
from app.core.database import engine, Base
from app.models.client import Client
from app.models.project import Project
from app.models.activity import Activity


async def reset_database():
    """Reset the database by dropping and recreating all tables"""
    print("Starting database reset...")

    async with engine.begin() as conn:
        print("Dropping existing tables...")
        await conn.run_sync(Base.metadata.drop_all)

        print("Recreating tables...")
        await conn.run_sync(Base.metadata.create_all)

    print("Database reset completed successfully!")


if __name__ == "__main__":
    asyncio.run(reset_database())
