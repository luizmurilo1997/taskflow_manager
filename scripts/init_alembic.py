import os
import shutil
from pathlib import Path


def init_alembic():
    """Initialize Alembic with custom template and configuration."""
    if os.path.exists('migrations'):
        shutil.rmtree('migrations')

    os.system('alembic init migrations')

    template_path = Path('scripts/alembic_template/env.py.template')
    if template_path.exists():
        shutil.copy(template_path, 'migrations/env.py')
        print("✅ Successfully initialized Alembic with async configuration")
    else:
        print("❌ Template file not found")


if __name__ == "__main__":
    init_alembic()
