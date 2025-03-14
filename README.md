# TaskFlow Manager API Documentation

## 1. Introduction

TaskFlow Manager is a comprehensive task management API built with modern technologies, designed to efficiently handle projects, activities, and client relationships. It provides a robust system for creating, updating, and managing various business entities while maintaining clear relationships and status tracking.

### Key Features

- Client management with API key authentication
- Project lifecycle tracking
- Activity management and monitoring
- Secure API endpoints with API key authentication
- Comprehensive OpenAPI documentation
- Clean architecture and layered design

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
│   │   ├── database.py # Database configuration
│   │   ├── deps.py     # Dependency injection
│   │   ├── logging_config.py # Logging configuration
│   │   └── security.py # Authentication and security
│   ├── models/         # SQLAlchemy database models
│   │   ├── activity.py
│   │   ├── client.py
│   │   └── project.py
│   ├── repositories/   # Data access layer
│   │   ├── activity_repository.py
│   │   ├── client_repository.py
│   │   └── project_repository.py
│   ├── routes/         # API endpoints
│   │   ├── activity_routes.py
│   │   ├── client_routes.py
│   │   └── project_routes.py
│   ├── schemas/        # Pydantic models for request/response
│   │   ├── activity.py
│   │   ├── client.py
│   │   └── project.py
│   └── services/       # Business logic layer
│       ├── activity_service.py
│       ├── client_service.py
│       └── project_service.py
├── migrations/         # Database migrations
│   ├── versions/      # Migration versions
│   └── env.py        # Alembic configuration
├── scripts/           # Utility scripts
│   ├── alembic_template/
│   ├── init_alembic.py
│   ├── reset_db.py
│   └── seed_db.py
├── tests/             # Test suite
│   ├── core/         # Core functionality tests
│   ├── integration/  # Integration tests
│   ├── models/       # Model tests
│   └── services/     # Service layer tests
├── .env.example      # Example environment variables
├── .gitignore        # Git ignore rules
├── alembic.ini       # Alembic configuration
├── docker-compose.yml # Docker configuration
├── pyproject.toml    # Project configuration
└── requirements.txt  # Project dependencies
```

## 4. First Time Setup

### 4.1 Prerequisites

- [Python 3.12 or higher](https://www.python.org/downloads/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (for Windows/macOS) or [Docker Engine](https://docs.docker.com/engine/install/) (for Linux)
- Git

### 4.2 Installation Steps

#### Option 1: Using Docker (Recommended)

1. **Clone the Repository**

   ```bash
   git clone <repository-url>
   cd taskflow-manager
   ```

2. **Start the Application**

   ```bash
   docker compose up -d
   ```

3. **Wait for Services**
   The API will be available at http://localhost:8000 after the services are ready (usually takes about 30 seconds)

#### Option 2: Local Development

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
python -m pytest tests/

# Run unit tests
python -m pytest tests/services tests/models tests/core

# Run integration tests
python -m pytest tests/integration

# Run all tests with coverage report
python -m pytest --cov=app tests/ --cov-report term-missing
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

### 6.3 Docker Development

```bash
# Build and start services
docker compose up -d --build

# View logs
docker compose logs -f

# Stop services
docker compose down

# Stop services and remove volumes
docker compose down -v

# Reset database
docker compose down -v
docker compose up -d
sleep 5
python scripts/reset_db.py  # Reset database if needed
python scripts/seed_db.py   # Populate with initial data if needed
```

### 6.4 CI/CD Pipeline

The project includes a GitHub Actions workflow that:

1. Runs unit and integration tests
2. Generates and uploads coverage reports
3. Builds and pushes Docker image on successful merge to main

Required GitHub Secrets for CI/CD:

- `DOCKER_HUB_USERNAME`: Your Docker Hub username
- `DOCKER_HUB_ACCESS_TOKEN`: Your Docker Hub access token

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
