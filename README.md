# TaskFlow Manager API Documentation

## 1. Introduction

TaskFlow Manager is a comprehensive task management API built with modern technologies, designed to efficiently handle projects, activities, and client relationships. It provides a robust system for creating, updating, and managing various business entities while maintaining clear relationships and status tracking.

### Key Features

- Client management with API key authentication
- Project lifecycle tracking
- Activity management and monitoring
- Secure API endpoints
- Comprehensive documentation
- Clean architecture design

---

## 2. Entity Relationship Diagram (ERD)

![image](https://github.com/user-attachments/assets/1632502f-9fcc-4b42-ba98-66c8441403c3)

---

## 3. Technical Architecture

### 3.1 Tech Stack

- **Backend Framework**: FastAPI 0.109.2
- **Database**: PostgreSQL 15+
- **ORM**: SQLAlchemy 2.0
- **Authentication**: API Key-based
- **Documentation**: OpenAPI (Swagger/ReDoc)
- **Migration Tool**: Alembic
- **Testing**: pytest

### 3.2 Project Structure

```
taskflow_manager/
├── app/
│   ├── core/           # Core configurations and utilities
│   │   ├── config.py   # Environment and app settings
│   │   ├── security.py # Authentication logic
│   │   └── deps.py     # Dependency injection
│   ├── models/         # SQLAlchemy database models
│   ├── repositories/   # Data access layer
│   ├── routes/         # API endpoints
│   ├── schemas/        # Pydantic models for request/response
│   └── services/       # Business logic layer
├── migrations/         # Database migrations
├── tests/              # Test suite
├── docker-compose.yml  # Docker configuration
└── requirements.txt    # Project dependencies
```

## 4. First Time Setup

### 4.1 Prerequisites

- [Python 3.12 or higher](https://www.python.org/downloads/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (for Windows/macOS) or [Docker Engine](https://docs.docker.com/engine/install/) (for Linux)
- Git

### 4.2 Installation Steps

#### Windows (PowerShell)

1. **Clone and Setup Environment**

   ```powershell
   # Clone repository
   git clone <repository-url>
   cd taskflow-manager

   # Create and activate virtual environment
   python -m venv .venv
   .venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Start Database**

   ```powershell
   docker compose down -v
   docker compose up -d
   Start-Sleep -Seconds 5
   ```

3. **Initialize Database**

   ```powershell
   python scripts/init_alembic.py
   python -m alembic revision --autogenerate -m "Initial migration"
   python -m alembic upgrade head
   ```

4. **Start the Application**
   ```powershell
   python -m uvicorn app.main:app --reload
   ```

#### Linux/macOS (Terminal)

1. **Clone and Setup Environment**

   ```bash
   git clone <repository-url>
   cd taskflow-manager

   # Create and activate virtual environment
   python3 -m venv .venv
   source .venv/bin/activate

   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Start Database**

   ```bash
   docker compose down -v
   docker compose up -d
   sleep 5
   ```

3. **Initialize Database**

   ```bash
   python scripts/init_alembic.py
   python -m alembic revision --autogenerate -m "Initial migration"
   python -m alembic upgrade head
   ```

4. **Start the Application**
   ```bash
   python -m uvicorn app.main:app --reload
   ```

## 5. Verify Installation

1. **Check API Status**
   Open your browser and access:

   - Main API: http://localhost:8000

2. **Access API Documentation**

   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

3. **Test Authentication**
   Use this API Key in your requests:
   ```
   X-API-Key: dev_api_key_super_secret
   ```

## 6. Development Guide

### 6.1 Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage report
python -m pytest --cov=app.services tests/ --cov-report term-missing
```

### 6.2 Database Management

```bash
# Create new migration
python -m alembic revision --autogenerate -m "Description"

# Apply migrations
python -m alembic upgrade head

# Rollback migration
python -m alembic downgrade -1
```

## 7. Troubleshooting

### 7.1 Database Issues

If you encounter database problems:

1. **Reset Database Container**

   ```bash
   docker compose down -v
   docker compose up -d
   sleep 5
   ```

2. **Reset Migrations**

   ```bash
   rm -rf migrations
   python scripts/init_alembic.py
   python -m alembic revision --autogenerate -m "Initial migration"
   python -m alembic upgrade head
   ```

### 7.2 Common Solutions

- Ensure Docker is running
- Check if port 5432 is available
- Verify database credentials in `.env`
- Make sure virtual environment is activated
- Use `python -m` prefix for commands on Windows

