import asyncio
import pytest
import pytest_asyncio
from typing import AsyncGenerator, Generator, Any, cast
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import Base, get_db

# Usar o PostgreSQL real para testes de integração
# Usando o mesmo nome de banco de dados que está configurado no CI/CD
DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/taskflow"


@pytest.fixture(scope="function")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Cria um novo event loop para cada teste."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def db_engine() -> AsyncGenerator[AsyncEngine, None]:
    """Cria um engine de banco de dados para cada teste."""
    engine = create_async_engine(DATABASE_URL, echo=False)

    yield engine

    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(db_engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:

    async_session_maker = sessionmaker(
        bind=db_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session_maker() as session:
        async with session.begin():

            yield session


@pytest_asyncio.fixture
async def test_client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Cria um cliente de teste com a sessão de banco de dados configurada."""

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        base_url="http://localhost:8000"
    ) as client:
        yield client

    app.dependency_overrides.clear()
