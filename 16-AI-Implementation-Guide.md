# 16-AI-Implementation-Guide.md

# Ahluwalia Growth OS

Version: 1.0

Status: Draft

Prepared By: Product & Engineering Team

Audience: Human Engineers and AI-Assisted Development Systems

---

# 1. Purpose

This document defines the implementation strategy for Ahluwalia Growth OS.

The objective is to ensure that any implementation team, regardless of tooling preferences, can consistently build the system according to the approved business, technical, and user experience specifications.

---

# 2. Guiding Philosophy

Implementation shall prioritize:

* Simplicity,
* Maintainability,
* Business alignment,
* Incremental delivery,
* Long-term extensibility.

The implementation team shall optimize for:

> Building the correct system before building the perfect system.

---

# 3. Source of Truth Hierarchy

Implementation decisions shall follow the following precedence order:

```text
Client Briefing PDF
↓
01-BRD.md
↓
02-FRS.md
↓
03-Data-Dictionary.md
↓
04-Business-Workflows.md
↓
05-State-Transition-Specification.md
↓
06-PRD.md
↓
07-User-Roles-Permissions.md
↓
08-Database-Design.md
↓
09-System-Architecture.md
↓
10-API-Specification.md
↓
11-UI-Screen-Specification.md
↓
12–15 Supporting Documents
```

If conflicts arise, higher-priority documents shall prevail.

---

# 4. Mandatory Constraints

Implementation teams shall NOT:

* Invent undocumented business workflows.
* Modify lifecycle transitions without approval.
* Circumvent role permissions.
* Embed business logic inside UI components.
* Access databases directly from API controllers.
* Introduce unnecessary architectural complexity.

---

# 5. Recommended Technology Stack

Frontend:

* Next.js
* TypeScript
* Tailwind CSS

Backend:

* FastAPI
* Python
* SQLAlchemy
* Alembic

Database:

* PostgreSQL

Storage:

* Cloudflare R2 or AWS S3

Authentication:

* JWT

---

# 6. Recommended Development Sequence

Phase 1:

Foundation.

Deliverables:

* Authentication.
* User Management.
* Role-Based Access Control.

---

Phase 2:

Field Operations.

Deliverables:

* Attendance.
* Site Discovery.
* Contact Management.

---

Phase 3:

Marketing Operations.

Deliverables:

* Meetings.
* Follow-Ups.
* Assignments.

---

Phase 4:

Sales Operations.

Deliverables:

* Showroom Visits.
* Opportunities.
* Lifecycle Management.

---

Phase 5:

Management Visibility.

Deliverables:

* Dashboards.
* Ownership Tracking.
* Reporting.

---

Phase 6:

Operational Enhancements.

Deliverables:

* Notifications.
* Audit Logging.
* Master Search.

---

# 7. Module Implementation Order

Recommended sequence:

1. Authentication
2. Users
3. Attendance
4. Sites
5. Contacts
6. Meetings
7. Assignments
8. Showroom Visits
9. Opportunities
10. Lifecycle
11. Ownership
12. Search
13. Dashboards
14. Notifications
15. Audit

---

# 8. Database Implementation Rules

Requirements:

* Follow documented schema definitions.
* Use UUID primary keys.
* Maintain referential integrity.
* Preserve historical records.

Prohibited:

* Direct schema modifications without migration scripts.
* Untracked database changes.

---

# 9. API Implementation Rules

Requirements:

* Follow documented endpoints.
* Enforce role permissions.
* Use standardized response structures.
* Validate all input data.

Prohibited:

* Business logic inside route handlers.
* Inconsistent response formats.

---

# 10. UI Implementation Rules

Requirements:

* Follow Apple-inspired simplicity principles.
* Prioritize mobile usability.
* Use progressive disclosure.
* Preserve consistency.

Common user actions should require no more than three interactions.

---

# 11. Business Workflow Rules

Implementation shall preserve:

* Opportunity ownership.
* Lifecycle progression.
* Revenue attribution.
* Assignment history.
* Stakeholder relationships.

---

# 12. Audit Requirements

The following activities must generate audit records:

* Lifecycle transitions.
* Assignments.
* Ownership changes.
* User administration actions.
* Opportunity updates.

Audit records shall remain immutable.

---

# 13. Testing Expectations

Required testing levels:

Unit Tests:

* Services.
* Lifecycle rules.
* Ownership logic.

---

Integration Tests:

* API endpoints.
* Database workflows.

---

End-to-End Tests:

* Site discovery journey.
* Opportunity conversion journey.
* Master search journey.

---

# 14. Security Expectations

Requirements:

* Password hashing.
* HTTPS.
* JWT expiration.
* Role validation.
* Input validation.

Prohibited:

* Hardcoded secrets.
* Plain-text credentials.
* Overly permissive access.

---

# 15. AI-Assisted Development Guardrails

AI-generated code shall:

* Respect architectural boundaries.
* Follow naming conventions.
* Preserve documentation intent.
* Include validation logic.
* Avoid unnecessary abstraction.

AI-generated code shall always undergo human review before production deployment.

---

# 16. Change Management Process

When requirements change:

Step 1:

Update BRD.

↓

Step 2:

Update FRS.

↓

Step 3:

Update affected technical documents.

↓

Step 4:

Implement changes.

Implementation shall never precede documentation updates.

---

# 17. Expansion Strategy

Future enhancements shall be introduced incrementally.

Potential future areas include:

* Architect Intelligence.
* Builder Intelligence.
* LMS Expansion.
* AI Forecasting.
* Predictive Analytics.

Future enhancements shall not compromise MVP simplicity.

---

# 18. Definition of Successful Implementation

The implementation effort shall be considered successful if the resulting system:

* Reflects Ahluwalia business processes.
* Remains easy to understand.
* Supports future expansion.
* Requires minimal user training.
* Encourages organizational adoption.

---

# 19. Success Statement

Growth OS implementation shall prioritize:

Building software that people actually use,

over

building software that merely satisfies specifications.

---

# End of Document
