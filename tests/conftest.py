import asyncio
import pytest
import pytest_asyncio
import sys
from typing import Generator


@pytest.fixture(scope="session")
def event_loop_policy() -> asyncio.AbstractEventLoopPolicy:
    if sys.platform.startswith('win'):
        policy = asyncio.WindowsSelectorEventLoopPolicy()
    else:
        policy = asyncio.DefaultEventLoopPolicy()
    asyncio.set_event_loop_policy(policy)
    return policy


@pytest_asyncio.fixture(scope="function")
def event_loop(event_loop_policy) -> Generator[asyncio.AbstractEventLoop, None, None]:
    loop = event_loop_policy.new_event_loop()
    yield loop
    loop.close()


def pytest_configure(config):
    """Configure pytest-asyncio to use function scope by default."""
    config.option.asyncio_mode = "strict"
    pytest_asyncio.fixture_scope_default = "function"
