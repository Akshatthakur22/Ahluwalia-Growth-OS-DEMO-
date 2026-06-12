# Ahluwalia Growth OS - Backend

FastAPI backend for Ahluwalia Growth OS.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Run database migrations:
```bash
alembic upgrade head
```

4. Start the server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Project Structure

```
backend/
├── app/
│   ├── api/           # API endpoints
│   ├── models/        # Database models
│   ├── schemas/       # Pydantic schemas
│   ├── repositories/  # Data access layer
│   ├── services/      # Business logic layer
│   ├── config.py      # Configuration
│   ├── database.py    # Database connection
│   └── main.py        # FastAPI application
├── alembic/           # Database migrations
├── tests/             # Test files
└── requirements.txt   # Python dependencies
```

## Architecture

The backend follows a modular monolith architecture with clear separation of concerns:

- **API Layer**: FastAPI routes and request/response handling
- **Service Layer**: Business logic and workflows
- **Repository Layer**: Database access and queries
- **Database**: PostgreSQL with SQLAlchemy ORM

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
