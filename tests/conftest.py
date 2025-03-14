import asyncio
import pytest
import platform
import inspect
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@pytest.fixture(scope="function")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.new_event_loop()

    asyncio.set_event_loop(loop)

    yield loop

    loop.close()


def pytest_configure(config):
    """Configure pytest-asyncio to use function scope by default."""
    config.option.asyncio_mode = "strict"


original_getsourcelines = inspect.getsourcelines


def patched_getsourcelines(obj):
    try:
        return original_getsourcelines(obj)
    except OSError:

        return (["def event_loop(): pass"], 1)


inspect.getsourcelines = patched_getsourcelines
