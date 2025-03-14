import asyncio
import os
import sys
import logging
from pathlib import Path


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("reset_db")

project_root = str(Path(__file__).parent.parent.absolute())
sys.path.insert(0, project_root)

try:
    from app.models.activity import Activity
    from app.models.project import Project
    from app.models.client import Client
    from app.core.database import engine, Base
except ImportError as e:
    logger.error(f"Error importing models or configurations: {e}")
    logger.error("Check if PYTHONPATH is configured correctly")
    sys.exit(1)


async def reset_database():
    """Reset the database by dropping and recreating all tables"""
    logger.info("Starting database reset...")

    if not engine or not engine.url:
        logger.error("Database URL not configured correctly")
        sys.exit(1)

    db_url_safe = str(engine.url).replace(
        str(engine.url.password or ''), '***')
    logger.info(f"Using database URL: {db_url_safe}")

    try:
        async with engine.begin() as conn:
            logger.info("Dropping existing tables...")
            await conn.run_sync(Base.metadata.drop_all)

            logger.info("Recreating tables...")
            await conn.run_sync(Base.metadata.create_all)

        logger.info("Database reset completed successfully!")
    except Exception as e:
        logger.error(f"Error during database reset: {e}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(reset_database())
    except Exception as e:
        logger.error(f"Error running reset_database: {e}")
        sys.exit(1)
