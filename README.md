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

## 2. Technical Architecture

### 2.1 Tech Stack

- **Backend Framework**: FastAPI 0.109.2
- **Database**: PostgreSQL 15+
- **ORM**: SQLAlchemy 2.0
- **Authentication**: API Key-based
- **Documentation**: OpenAPI (Swagger/ReDoc)
- **Migration Tool**: Alembic
- **Testing**: pytest

### 2.2 Project Structure

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
├── tests/             # Test suite
├── docker-compose.yml # Docker configuration
└── requirements.txt   # Project dependencies
```

## 3. First Time Setup (Windows)

### 3.1 Prerequisites

- [Python 3.12 or higher](https://www.python.org/downloads/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Git

### 3.2 Installation Steps

1. **Clone and Setup Environment**

   ```powershell
   # Clone repository
   git clone <repository-url>
   cd taskflow-manager

   # Create and activate virtual environment
   python -m venv .venv
   .venv\Scripts\activate.ps1

   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Start Database**

   ```powershell
   # Remove any existing containers (if any)
   docker compose down -v

   # Start fresh PostgreSQL container
   docker compose up -d

   # Wait a few seconds for the database to be ready
   Start-Sleep -Seconds 5
   ```

3. **Initialize Database**

   ```powershell
   # Initialize Alembic with our template
   python scripts/init_alembic.py

   # Create and apply initial migration
   python -m alembic revision --autogenerate -m "Initial migration"
   python -m alembic upgrade head
   ```

4. **Start the Application**
   ```powershell
   # Start FastAPI server with hot reload
   python -m uvicorn app.main:app --reload
   ```

### 3.3 Verify Installation

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

## 4. Development Guide

### 4.1 Running Tests

```powershell
# Run all tests
python -m pytest

# Run with coverage report
python -m pytest --cov=app.services tests/ --cov-report term-missing
```

### 4.2 Database Management

```powershell
# Create new migration
python -m alembic revision --autogenerate -m "Description"

# Apply migrations
python -m alembic upgrade head

# Rollback migration
python -m alembic downgrade -1
```

## 5. Troubleshooting

### 5.1 Database Issues

If you encounter database problems:

1. **Reset Database Container**

   ```powershell
   # Stop and remove container
   docker compose down -v

   # Start fresh container
   docker compose up -d
   Start-Sleep -Seconds 5
   ```

2. **Reset Migrations**

   ```powershell
   # Remove migrations folder
   Remove-Item -Recurse -Force migrations

   # Reinitialize migrations
   python scripts/init_alembic.py
   python -m alembic revision --autogenerate -m "Initial migration"
   python -m alembic upgrade head
   ```

### 5.2 Common Solutions

- Ensure Docker Desktop is running
- Check if port 5432 is available
- Verify database credentials in `.env`
- Make sure virtual environment is activated
- Use `python -m` prefix for commands in Windows
