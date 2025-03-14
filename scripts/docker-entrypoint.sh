#!/bin/bash
set -e

# Aguardar o PostgreSQL estar pronto
echo "Waiting for PostgreSQL to be ready..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "PostgreSQL is ready!"

# Inicializar Alembic se necessário
if [ ! -d "migrations" ]; then
    echo "Initializing Alembic..."
    python scripts/init_alembic.py
    
    # Configurar alembic.ini com a URL correta do banco
    sed -i "s#sqlalchemy.url = driver://user:pass@localhost/dbname#sqlalchemy.url = postgresql+asyncpg://postgres:postgres@db:5432/taskflow#" alembic.ini
    
    echo "Creating initial migration..."
    python -m alembic revision --autogenerate -m "Initial migration"
fi

# Aplicar migrações pendentes
echo "Applying migrations..."
python -m alembic upgrade head

# Iniciar a aplicação
echo "Starting FastAPI application..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 