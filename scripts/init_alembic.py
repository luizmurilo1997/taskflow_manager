import os
import sys
import shutil
import subprocess
from pathlib import Path


def init_alembic():
    """Initialize Alembic with custom template and configuration."""

    project_root = Path(__file__).parent.parent.absolute()

    migrations_dir = project_root / 'migrations'
    template_path = project_root / 'scripts' / \
        'alembic_template' / 'env.py.template'

    print(f"Diretório do projeto: {project_root}")
    print(f"Diretório de migrações: {migrations_dir}")
    print(f"Caminho do template: {template_path}")

    if migrations_dir.exists():
        print(f"Removendo diretório de migrações existente: {migrations_dir}")
        shutil.rmtree(migrations_dir)

    os.chdir(project_root)


    print("Inicializando Alembic...")
    result = subprocess.run(['alembic', 'init', 'migrations'],
                            capture_output=True,
                            text=True)

    if result.returncode != 0:
        print(f"❌ Erro ao inicializar Alembic: {result.stderr}")
        sys.exit(1)

    if template_path.exists():
        target_env_path = migrations_dir / 'env.py'
        print(f"Copiando template para: {target_env_path}")
        shutil.copy(template_path, target_env_path)
        print("✅ Alembic inicializado com sucesso usando configuração assíncrona")
    else:
        print(f"❌ Arquivo de template não encontrado: {template_path}")
        sys.exit(1)


if __name__ == "__main__":
    init_alembic()
