# 15-Engineering-Standards.md

# Ahluwalia Growth OS

Version: 1.0

Status: Draft

Prepared By: Product & Engineering Team

Applies To: All contributors, AI coding assistants, and future engineering teams

---

# 1. Purpose

This document defines the engineering standards governing the development of Ahluwalia Growth OS.

The objective is to ensure consistency, maintainability, scalability, and long-term code quality.

---

# 2. Engineering Philosophy

Growth OS shall prioritize:

* Simplicity over cleverness,
* Readability over brevity,
* Maintainability over premature optimization,
* Consistency over personal preference.

---

# 3. Core Principles

## ES-001

Code shall optimize for future maintainers.

---

## ES-002

Business logic shall never reside in UI components.

---

## ES-003

Database access shall occur only through repositories.

---

## ES-004

All critical actions shall be auditable.

---

## ES-005

Security shall be built-in, not bolted on.

---

# 4. Architecture Standards

Architecture Style:

Modular Monolith.

---

Required Layers:

```text id="wks0h0"
API Layer
↓
Service Layer
↓
Repository Layer
↓
Database
```

---

Forbidden:

* Direct database access from API routes.
* Business logic inside controllers.
* Cross-module circular dependencies.

---

# 5. Backend Standards

Technology Stack:

* Python
* FastAPI
* SQLAlchemy
* Alembic
* PostgreSQL

---

Requirements:

* Type hints mandatory.
* Dependency injection preferred.
* Services shall remain stateless.
* Transactions shall be explicit.

---

# 6. Frontend Standards

Technology Stack:

* Next.js
* TypeScript
* Tailwind CSS

---

Requirements:

* Strict TypeScript mode enabled.
* Components shall remain focused.
* Business logic shall reside outside UI components.
* Shared components shall be reusable.

---

# 7. API Standards

APIs shall:

* Be RESTful.
* Use JSON.
* Follow versioning conventions.
* Return standardized responses.

---

Response Format:

Success:

```json
{
  "success": true,
  "data": {},
  "message": ""
}
```

Error:

```json
{
  "success": false,
  "error_code": "",
  "message": ""
}
```

---

# 8. Database Standards

Requirements:

* UUID primary keys preferred.
* Foreign keys mandatory.
* Indexes added intentionally.
* Soft deletes evaluated case-by-case.
* Historical data preserved.

---

Prohibited:

* Orphan records.
* Unindexed search fields.
* Hidden business rules within SQL triggers.

---

# 9. Naming Standards

Database Tables:

```text id="u0s96t"
snake_case
plural nouns
```

Examples:

```text id="4d3xni"
users
sites
opportunities
```

---

Python Files:

```text id="2rpld7"
snake_case.py
```

---

React Components:

```text id="nnivws"
PascalCase.tsx
```

---

Variables:

```text id="5j50rl"
camelCase
```

---

Constants:

```text id="0z41ca"
UPPER_SNAKE_CASE
```

---

# 10. Logging Standards

Operational logs shall include:

* Timestamp.
* Severity.
* Correlation ID.
* Message.

---

Sensitive information shall never be logged.

---

# 11. Audit Standards

Audit logs shall be generated for:

* Lifecycle transitions.
* Assignment changes.
* Ownership changes.
* Administrative actions.

---

Audit events shall remain immutable.

---

# 12. Security Standards

Requirements:

* Password hashing mandatory.
* HTTPS required.
* JWT expiration enforced.
* RBAC validation applied.

---

Prohibited:

* Plain-text credentials.
* Hardcoded secrets.
* Overly permissive authorization.

---

# 13. Testing Standards

Required Testing Types:

* Unit Tests.
* Integration Tests.
* API Tests.

---

Critical Areas Requiring Tests:

* Lifecycle transitions.
* Permission validation.
* Ownership attribution.
* Search functionality.

---

# 14. Error Handling Standards

Errors shall:

* Be user-friendly.
* Avoid exposing internal details.
* Be logged appropriately.
* Use standardized formats.

---

# 15. Git Standards

Branch Naming:

```text id="s7ifpi"
feature/

bugfix/

hotfix/
```

Examples:

```text id="i6cqhm"
feature/site-discovery

bugfix/search-indexing
```

---

Commit Messages:

Format:

```text id="15vjlwm"
type(scope): description
```

Examples:

```text id="xjlwm0"
feat(sites): add site capture workflow

fix(search): improve mobile lookup
```

---

# 16. Documentation Standards

Requirements:

* Public APIs documented.
* Major architectural decisions recorded.
* Complex business rules explained.
* README maintained.

---

# 17. Performance Standards

API Target:

Less than 500 ms average response time.

---

Search Target:

Less than 1 second.

---

Dashboard Target:

Less than 3 seconds.

---

# 18. Code Review Standards

Reviews shall evaluate:

* Correctness.
* Security.
* Maintainability.
* Performance.
* Alignment with documented requirements.

---

Personal preferences shall not override standards.

---

# 19. AI-Assisted Development Standards

Claude/Cursor generated code shall:

* Follow documented architecture.
* Respect module boundaries.
* Include appropriate validation.
* Avoid introducing hidden dependencies.

---

AI-generated code shall undergo human review.

---

# 20. Definition of Engineering Success

Growth OS engineering shall be considered successful if the system is:

* Easy to understand,
* Easy to extend,
* Easy to test,
* Easy to maintain,
* Difficult to misuse.

---

# End of Document
