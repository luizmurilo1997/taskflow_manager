import asyncio
import os
import pytest
import pytest_asyncio
from typing import AsyncGenerator, Generator, Any, cast
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import Base, get_db

# Use environment variables with fallbacks
DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/taskflow")
BASE_URL = os.environ.get("BASE_URL", "http://localhost:8000")
USE_IN_PROCESS = os.environ.get(
    "USE_IN_PROCESS_TESTING", "false").lower() == "true"

print(f"Integration tests using DATABASE_URL: {DATABASE_URL}")
print(f"Integration tests using BASE_URL: {BASE_URL}")
print(f"Using in-process testing: {USE_IN_PROCESS}")


@pytest_asyncio.fixture(scope="function")
async def db_engine() -> AsyncGenerator[AsyncEngine, None]:
    """Create a database engine for each test."""
    engine = create_async_engine(DATABASE_URL, echo=False)

    yield engine

    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(db_engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    """Create a database session for each test."""
    async_session_maker = sessionmaker(
        bind=db_engine, class_=AsyncSession, expire_on_commit=False
    )

    # Não usar o bloco 'async with session.begin()' aqui
    # pois isso fecha a transação automaticamente ao sair do bloco
    session = async_session_maker()
    try:
        yield session
    finally:
        await session.close()


@pytest_asyncio.fixture
async def test_client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create a test client with the database session configured."""

    async def override_get_db():
        try:
            yield db_session
        except Exception as e:
            await db_session.rollback()
            raise e

    app.dependency_overrides[get_db] = override_get_db

    # Configuração do cliente de teste
    client_params = {}

    # Se estiver usando testes in-process, use o app diretamente
    if USE_IN_PROCESS:
        client_params["app"] = app
        client_params["base_url"] = "http://testserver"
    else:
        client_params["base_url"] = BASE_URL

    async with AsyncClient(**client_params) as client:
        # Add default headers for all requests
        client.headers.update(
            {"X-API-Key": os.environ.get("API_KEY", "dev_api_key_super_secret")})
        yield client

    app.dependency_overrides.clear()
