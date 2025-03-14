import asyncio
from datetime import datetime, timezone
from app.core.database import engine, Base
from app.models.client import Client
from app.models.project import Project
from app.models.activity import Activity
from app.core.security import get_password_hash
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db


async def seed_database():
    """Populate the database with initial example data"""
    print("Starting database seeding...")

    async with AsyncSession(engine) as session:
        print("Creating clients...")
        clients = [
            Client(
                name="Microsoft Corporation",
                email="contact@microsoft.com",
                hashed_password=get_password_hash("microsoft123")
            ),
            Client(
                name="Google LLC",
                email="contact@google.com",
                hashed_password=get_password_hash("google123")
            ),
            Client(
                name="Apple Inc",
                email="contact@apple.com",
                hashed_password=get_password_hash("apple123")
            )
        ]

        for client in clients:
            session.add(client)
        await session.commit()

        print("Creating projects...")
        projects = [
            Project(
                name="Enterprise Management System",
                description="Complete enterprise management system",
                status="In Progress",
                client_id=1
            ),
            Project(
                name="Mobile Application",
                description="Cross-platform mobile application",
                status="Open",
                client_id=1
            ),
            Project(
                name="Web Portal",
                description="Responsive web portal",
                status="In Progress",
                client_id=2
            )
        ]

        for project in projects:
            session.add(project)
        await session.commit()

        print("Creating activities...")
        activities = [
            Activity(
                description="Requirements analysis",
                project_id=1,
                start_time=datetime.now(timezone.utc)
            ),
            Activity(
                description="Backend development",
                project_id=1,
                start_time=datetime.now(timezone.utc)
            ),
            Activity(
                description="Interface design",
                project_id=2,
                start_time=datetime.now(timezone.utc)
            )
        ]

        for activity in activities:
            session.add(activity)
        await session.commit()

    print("Database seeding completed successfully!")


if __name__ == "__main__":
    asyncio.run(seed_database())
