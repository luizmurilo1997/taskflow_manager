import asyncio
import os
import sys
import logging
from pathlib import Path

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("reset_db")

# Add the project root directory to Python path
project_root = str(Path(__file__).parent.parent.absolute())
sys.path.insert(0, project_root)

try:
    from app.models.activity import Activity
    from app.models.project import Project
    from app.models.client import Client
    from app.core.database import engine, Base
except ImportError as e:
    logger.error(f"Erro ao importar modelos ou configurações: {e}")
    logger.error("Verifique se o PYTHONPATH está configurado corretamente")
    sys.exit(1)


async def reset_database():
    """Reset the database by dropping and recreating all tables"""
    logger.info("Iniciando reset do banco de dados...")

    # Verificar se a URL do banco de dados está definida
    if not engine or not engine.url:
        logger.error("URL do banco de dados não configurada corretamente")
        sys.exit(1)

    # Mostrar a URL do banco (ocultando a senha)
    db_url_safe = str(engine.url).replace(
        str(engine.url.password or ''), '***')
    logger.info(f"Usando URL do banco: {db_url_safe}")

    try:
        async with engine.begin() as conn:
            logger.info("Removendo tabelas existentes...")
            await conn.run_sync(Base.metadata.drop_all)

            logger.info("Recriando tabelas...")
            await conn.run_sync(Base.metadata.create_all)

        logger.info("Reset do banco de dados concluído com sucesso!")
    except Exception as e:
        logger.error(f"Erro durante o reset do banco de dados: {e}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(reset_database())
    except Exception as e:
        logger.error(f"Erro ao executar reset_database: {e}")
        sys.exit(1)
