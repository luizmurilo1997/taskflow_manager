# Remover todas as importações para evitar referências circulares

from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Removendo as importações circulares

# Isso garante que todos os modelos sejam carregados na ordem correta
