# 10-API-Specification.md

# Ahluwalia Growth OS

Version: 1.0

Status: Draft

Prepared By: Product & Engineering Team

Based On: BRD v1.0, FRS v1.0, Database Design v1.0

---

# 1. Purpose

This document defines the REST API specification for Ahluwalia Growth OS.

The objective is to provide implementation-ready contracts for frontend applications, backend development, and AI-assisted code generation.

---

# 2. API Principles

1. APIs shall expose business capabilities.
2. APIs shall be RESTful.
3. APIs shall use JSON.
4. APIs shall enforce role-based authorization.
5. APIs shall preserve auditability.
6. APIs shall remain backward compatible where possible.

---

# 3. Authentication APIs

Base Path:

/api/v1/auth

---

POST /login

Purpose:

Authenticate users.

Request:

* mobile_number
* password

Response:

* access_token
* user_information
* permissions

---

POST /logout

Purpose:

Terminate active session.

---

GET /me

Purpose:

Retrieve current user information.

---

# 4. Attendance APIs

Base Path:

/api/v1/attendance

---

POST /check-in

Purpose:

Record attendance.

Request:

* latitude
* longitude
* device_information

Response:

* attendance_status
* check_in_time

---

GET /my-attendance

Purpose:

Retrieve personal attendance history.

---

GET /team-attendance

Purpose:

Manager attendance visibility.

Authorization:

Manager, CEO.

---

# 5. Site APIs

Base Path:

/api/v1/sites

---

POST /

Purpose:

Create new site.

---

GET /

Purpose:

Retrieve accessible sites.

---

GET /{site_id}

Purpose:

Retrieve site details.

---

PATCH /{site_id}

Purpose:

Update site information.

---

POST /{site_id}/media

Purpose:

Upload site evidence.

---

# 6. Contact APIs

Base Path:

/api/v1/contacts

---

POST /

Purpose:

Create stakeholder.

---

GET /

Purpose:

Retrieve contacts.

---

GET /{contact_id}

Purpose:

Retrieve contact details.

---

PATCH /{contact_id}

Purpose:

Update contact.

---

# 7. Meeting APIs

Base Path:

/api/v1/meetings

---

POST /

Purpose:

Record meeting.

---

GET /

Purpose:

Retrieve meetings.

---

PATCH /{meeting_id}

Purpose:

Update meeting.

---

# 8. Assignment APIs

Base Path:

/api/v1/assignments

---

POST /

Purpose:

Assign opportunities.

Authorization:

Manager.

---

GET /

Purpose:

Retrieve assignments.

---

# 9. Showroom APIs

Base Path:

/api/v1/showroom-visits

---

POST /

Purpose:

Schedule showroom visit.

---

GET /

Purpose:

Retrieve showroom visits.

---

PATCH /{visit_id}

Purpose:

Update showroom visit outcomes.

---

# 10. Opportunity APIs

Base Path:

/api/v1/opportunities

---

POST /

Purpose:

Create opportunity.

---

GET /

Purpose:

Retrieve opportunities.

---

GET /{opportunity_id}

Purpose:

Retrieve opportunity details.

---

PATCH /{opportunity_id}

Purpose:

Update opportunity.

---

POST /{opportunity_id}/transition

Purpose:

Transition lifecycle state.

Request:

* new_status
* remarks

Response:

* previous_status
* new_status
* transition_timestamp

---

# 11. Lifecycle APIs

Base Path:

/api/v1/lifecycle

---

GET /history/{opportunity_id}

Purpose:

Retrieve lifecycle history.

---

# 12. Ownership APIs

Base Path:

/api/v1/ownership

---

GET /{opportunity_id}

Purpose:

Retrieve ownership chain.

---

PATCH /{opportunity_id}

Purpose:

Update ownership information.

Authorization:

Manager.

---

# 13. Architect APIs

Base Path:

/api/v1/architects

---

GET /

Purpose:

Retrieve architect profiles.

---

GET /{architect_id}

Purpose:

Retrieve architect details.

---

PATCH /{architect_id}

Purpose:

Update architect intelligence.

---

# 14. Builder APIs

Base Path:

/api/v1/builders

---

GET /

Purpose:

Retrieve builder profiles.

---

GET /{builder_id}

Purpose:

Retrieve builder details.

---

PATCH /{builder_id}

Purpose:

Update builder intelligence.

---

# 15. LMS APIs

Base Path:

/api/v1/training

---

GET /programs

Purpose:

Retrieve training programs.

---

GET /my-progress

Purpose:

Retrieve learning progress.

---

POST /assessments/{assessment_id}/submit

Purpose:

Submit assessments.

---

# 16. Search APIs

Base Path:

/api/v1/search

---

GET /mobile/{mobile_number}

Purpose:

Retrieve complete customer history.

Response May Include:

* Contacts
* Sites
* Meetings
* Showroom Visits
* Opportunities
* Ownership Information

---

GET /name/{name}

Purpose:

Search by stakeholder name.

---

# 17. Dashboard APIs

Base Path:

/api/v1/dashboard

---

GET /manager

Purpose:

Retrieve managerial dashboards.

Authorization:

Manager.

---

GET /executive

Purpose:

Retrieve CEO dashboards.

Authorization:

CEO.

---

# 18. Notification APIs

Base Path:

/api/v1/notifications

---

GET /

Purpose:

Retrieve notifications.

---

PATCH /{notification_id}/read

Purpose:

Mark notification as read.

---

# 19. Audit APIs

Base Path:

/api/v1/audit

---

GET /

Purpose:

Retrieve audit logs.

Authorization:

Administrator.

---

# 20. Standard Response Format

Success Response:

{
"success": true,
"data": {},
"message": ""
}

---

Error Response:

{
"success": false,
"error_code": "",
"message": ""
}

---

# 21. Authorization Strategy

Field Executive:

* Attendance
* Site Discovery

---

Marketing Executive:

* Meetings
* Showroom Requests

---

Sales Executive:

* Showroom Activities
* Opportunity Conversion

---

Manager:

* Assignments
* Team Visibility

---

CEO:

* Dashboard Visibility

---

Administrator:

* System Administration

---

# 22. API Versioning Strategy

Current Version:

v1

Base URL:

/api/v1

Future Strategy:

Introduce v2 only for breaking changes.

---

# 23. Non-Functional Requirements

* Average response time < 500 ms.
* JWT-based authentication.
* HTTPS mandatory.
* Audit logging for critical actions.
* Pagination support for list endpoints.

---

# End of Document
