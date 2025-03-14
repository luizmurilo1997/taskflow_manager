import asyncio
import httpx
import os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/taskflow")
BASE_URL = os.environ.get("BASE_URL", "http://localhost:8000")


async def test_database_connection():
    """Test connection to the database."""
    print(f"Connecting to database: {DATABASE_URL}")
    engine = create_async_engine(DATABASE_URL, echo=False)

    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            value = result.scalar()
            print(f"Database connection successful: {value}")

            # Check if tables exist
            result = await conn.execute(
                text(
                    "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
            )
            tables = [row[0] for row in result.fetchall()]
            print(f"Tables in database: {tables}")

            return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False
    finally:
        await engine.dispose()


async def test_api_connection():
    """Test connection to the API."""
    print(f"Connecting to API: {BASE_URL}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/")
            print(f"API connection status: {response.status_code}")
            print(f"API response: {response.text}")

            return response.status_code == 200
    except Exception as e:
        print(f"API connection failed: {e}")
        return False


async def main():
    """Run all tests."""
    db_success = await test_database_connection()
    api_success = await test_api_connection()

    print("\nTest Results:")
    print(f"Database Connection: {'✅ Success' if db_success else '❌ Failed'}")
    print(f"API Connection: {'✅ Success' if api_success else '❌ Failed'}")

    if db_success and api_success:
        print("\n✅ All connections successful!")
    else:
        print("\n❌ Some connections failed!")


if __name__ == "__main__":
    asyncio.run(main())
