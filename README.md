# Ahluwalia Growth OS

Business Operating System for Ahluwalia Marbles.

## Overview

Ahluwalia Growth OS is a centralized business operating platform designed to streamline and digitize core operations including employee attendance, field-force activities, marketing efforts, showroom sales processes, training initiatives, and management reporting.

## Project Structure

```
Ahluwalia-Growth-OS-DEMO-/
├── backend/           # FastAPI backend
├── frontend/          # Next.js frontend
├── 01-BRD.md         # Business Requirements Document
├── 02-FRS.md/        # Functional Requirements
├── 03-Data-Dictionary.md
├── 04-Business-Workflows.md
├── 05-State-Transition-Specification.md
├── 06-PRD.md         # Product Requirements Document
├── 07-User-Roles-Permissions.md
├── 08-Database-Design.md
├── 09-System-Architecture.md
├── 10-API-Specification.md
├── 11-UI-Screen-Specification.md
├── 12-Audit-Logging-Specification.md
├── 13-Master-Search-Specification.md
├── 14-Dashboard-Metrics-Specification.md
├── 15-Engineering-Standards.md
├── 16-AI-Implementation-Guide.md
└── 17-Definition-of-Done.md
```

## Technology Stack

### Backend
- FastAPI (Python)
- SQLAlchemy ORM
- PostgreSQL
- Alembic (migrations)
- JWT Authentication

### Frontend
- Next.js 14
- TypeScript
- Tailwind CSS
- Axios
- Zustand

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

4. Run migrations:
```bash
alembic upgrade head
```

5. Start server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Configure environment:
```bash
cp .env.local.example .env.local
```

4. Start development server:
```bash
npm run dev
```

## API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## User Roles

- Field Executive
- Marketing Executive
- Sales Executive
- Manager
- CEO
- Administrator

## Core Features

### MVP (Phase 1)
- Authentication & User Management
- Attendance & Live Tracking
- Site Discovery Module
- Marketing CRM
- Showroom Visit Module
- Opportunity Management
- Master Search
- Dashboard Module

### Phase 2 (Future)
- Architect Growth Engine
- Builder Command Center
- LMS Module

## Development Guidelines

All development must follow the specifications in the documentation:
- Engineering Standards (15-Engineering-Standards.md)
- API Specification (10-API-Specification.md)
- Database Design (08-Database-Design.md)
- UI Specification (11-UI-Screen-Specification.md)

## License

Proprietary - Ahluwalia Marbles
