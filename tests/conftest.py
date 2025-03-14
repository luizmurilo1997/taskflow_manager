import asyncio
import pytest
import platform
import inspect
import os
import sys

# Adicionar o diretório raiz ao PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

# Configurar a política de loop de eventos para Windows
if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@pytest.fixture(scope="function")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    # Criar um novo loop de eventos
    loop = asyncio.new_event_loop()

    # Definir o loop como o loop atual
    asyncio.set_event_loop(loop)

    # Retornar o loop para o teste
    yield loop

    # Fechar o loop após o teste
    loop.close()


def pytest_configure(config):
    """Configure pytest-asyncio to use function scope by default."""
    config.option.asyncio_mode = "strict"


# Monkey patch para evitar o erro "could not get source code"
original_getsourcelines = inspect.getsourcelines


def patched_getsourcelines(obj):
    try:
        return original_getsourcelines(obj)
    except OSError:
        # Retornar código fonte fictício para evitar o erro
        return (["def event_loop(): pass"], 1)


inspect.getsourcelines = patched_getsourcelines
