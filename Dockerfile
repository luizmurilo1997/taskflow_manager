FROM python:3.12-slim

WORKDIR /app

# Instalar netcat
RUN apt-get update && apt-get install -y netcat-traditional && rm -rf /var/lib/apt/lists/*

# Copiar apenas os arquivos necessários primeiro
COPY requirements.txt .
COPY pyproject.toml .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o resto do código
COPY . .

# Tornar o script de entrypoint executável
RUN chmod +x scripts/docker-entrypoint.sh

# Expor a porta 8000
EXPOSE 8000

# Usar o script de entrypoint
ENTRYPOINT ["./scripts/docker-entrypoint.sh"]