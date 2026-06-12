# 07-User-Roles-Permissions.md

# Ahluwalia Growth OS

Version: 1.0

Status: Draft

Prepared By: Product & Engineering Team

Based On: BRD v1.0, FRS v1.0, Client Briefing PDF

---

# 1. Purpose

This document defines the user roles and associated permissions within Ahluwalia Growth OS.

The objective is to ensure:

* Appropriate access control,
* Clear ownership responsibilities,
* Protection of business data,
* Role-based visibility across modules.

---

# 2. Role Definitions

## 2.1 Field Executive

Primary Objective:

Identify and capture new opportunities from the field.

Responsibilities:

* Discover new sites.
* Capture stakeholder information.
* Upload site evidence.
* Maintain field activity records.

---

## 2.2 Marketing Executive

Primary Objective:

Build relationships and nurture opportunities.

Responsibilities:

* Conduct meetings.
* Maintain relationship history.
* Schedule follow-ups.
* Request showroom visits.

---

## 2.3 Sales Executive

Primary Objective:

Convert opportunities into revenue.

Responsibilities:

* Conduct showroom engagements.
* Record selections.
* Share quotations.
* Negotiate opportunities.
* Confirm orders.

---

## 2.4 Manager

Primary Objective:

Coordinate execution and monitor teams.

Responsibilities:

* Allocate opportunities.
* Review team activities.
* Monitor pipeline progression.
* Access dashboards.

---

## 2.5 CEO

Primary Objective:

Gain strategic visibility into organizational performance.

Responsibilities:

* Monitor business health.
* Review executive dashboards.
* Evaluate organizational performance.

---

## 2.6 Administrator (Derived Role)

Source:

Derived Implementation Requirement.

Primary Objective:

Manage system configuration and user administration.

Responsibilities:

* User management.
* Role assignment.
* System maintenance.

---

# 3. Permission Levels

The following permission levels shall be used.

| Permission | Meaning            |
| ---------- | ------------------ |
| View       | Read information   |
| Create     | Add new records    |
| Update     | Modify records     |
| Delete     | Remove records     |
| Assign     | Allocate ownership |
| Approve    | Authorize actions  |
| Export     | Download reports   |

---

# 4. Permissions Matrix

| Module            | Field Exec       | Marketing             | Sales           | Manager        | CEO          | Admin |
| ----------------- | ---------------- | --------------------- | --------------- | -------------- | ------------ | ----- |
| Attendance        | Create, View Own | View Own              | View Own        | View Team      | View Reports | Full  |
| Site Discovery    | Create, View Own | View Assigned         | View Assigned   | Full           | View Reports | Full  |
| Meetings          | View             | Create, Update        | View            | Full           | View Reports | Full  |
| Showroom Requests | View             | Create                | View            | Approve        | View Reports | Full  |
| Showroom Visits   | View             | View                  | Create, Update  | Full           | View Reports | Full  |
| Opportunities     | View Own         | View Assigned         | Update Assigned | Full           | View Reports | Full  |
| Lifecycle Updates | No               | Relationship Building | Sales Stages    | Override       | View         | Full  |
| Assignments       | No               | View                  | View            | Create, Assign | View         | Full  |
| Dashboards        | No               | No                    | No              | Full           | Full         | Full  |
| LMS               | View Own         | View Own              | View Own        | View Team      | View Reports | Full  |
| User Management   | No               | No                    | No              | No             | No           | Full  |

---

# 5. Role Visibility Rules

## RVR-001

Field Executives shall only access information associated with opportunities they created.

---

## RVR-002

Marketing Executives shall only access opportunities assigned to them.

---

## RVR-003

Sales Executives shall only access opportunities allocated to them.

---

## RVR-004

Managers shall have access to information associated with teams under their supervision.

---

## RVR-005

CEOs shall have organization-wide reporting visibility.

---

## RVR-006

Administrators shall possess unrestricted system access.

---

# 6. Lifecycle Permissions

| Lifecycle State          | Responsible Role          |
| ------------------------ | ------------------------- |
| New Site                 | Field Executive           |
| Relationship Building    | Marketing Executive       |
| Showroom Visit Scheduled | Marketing Executive       |
| Showroom Visit Done      | Sales Executive           |
| Selection Done           | Sales Executive           |
| Quotation Sent           | Sales Executive           |
| Negotiation              | Sales Executive           |
| Order Confirmed          | Sales Executive           |
| Lost                     | Sales Executive / Manager |

---

# 7. Dashboard Access Rules

## Managers

May access:

* Attendance reports.
* Team productivity reports.
* Pipeline reports.
* Lifecycle reports.
* Assignment reports.

---

## CEO

May access:

* Organization-wide dashboards.
* Revenue visibility.
* Team performance visibility.
* Pipeline health indicators.
* Strategic growth indicators.

---

# 8. Derived Permissions

The following permissions represent implementation decisions and are not explicitly stated within the PDF.

* Administrator role.
* Export permissions.
* Delete permissions.
* Approval permissions.
* Manager override permissions.

These items require stakeholder validation.

---

# 9. Open Questions

The following items require stakeholder clarification.

1. Should Managers edit records created by subordinates?
2. Should deleted records be recoverable?
3. Can opportunities be reassigned between teams?
4. Should CEOs possess read-only access?
5. Should temporary access delegation be supported?
6. Should external consultants access the system?

---

# 10. Guiding Principles

1. Least privilege access shall be enforced.
2. Ownership visibility shall be preserved.
3. Role responsibilities shall remain distinct.
4. Executive access shall prioritize reporting.
5. Derived permissions shall require stakeholder approval.

---

# End of Document
