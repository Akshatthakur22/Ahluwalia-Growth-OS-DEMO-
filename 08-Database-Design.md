# 08-Database-Design.md

# Ahluwalia Growth OS

Version: 1.0

Status: Draft

Prepared By: Product & Engineering Team

Based On: BRD v1.0, FRS v1.0, Client Briefing PDF

---

# 1. Purpose

This document defines the logical database design for Ahluwalia Growth OS.

The objective is to establish a scalable, maintainable, and implementation-ready data model that supports current MVP requirements while enabling future expansion.

---

# 2. Database Design Principles

1. Model the business process, not the screens.
2. Maintain a single source of truth.
3. Preserve historical information.
4. Minimize unnecessary duplication.
5. Optimize for MVP simplicity and future scalability.
6. Support auditability and reporting.
7. Enable mobile-number-driven search.

---

# 3. Database Overview

The proposed database consists of the following entities:

| Category                | Tables                               |
| ----------------------- | ------------------------------------ |
| Security                | users, roles                         |
| Attendance              | attendance_logs                      |
| Opportunity Discovery   | sites, contacts, site_media          |
| Relationship Management | meetings                             |
| Ownership & Assignment  | assignments, ownership_records       |
| Showroom Operations     | showroom_visits                      |
| Opportunity Management  | opportunities, lifecycle_history     |
| Strategic Intelligence  | architect_profiles, builder_profiles |
| Learning                | training_programs, training_progress |
| Reporting & Audit       | dashboard_snapshots, audit_logs      |
| Supporting              | notifications                        |

---

# 4. Core Tables

---

## users

Purpose:

Stores employee information.

Key Fields:

* id (UUID)
* employee_code
* full_name
* mobile_number
* email
* role_id
* manager_id
* status
* assigned_region
* created_at

Relationships:

* One user has many attendance_logs.
* One user creates many sites.
* One user participates in meetings.
* One user receives assignments.

---

## roles

Purpose:

Defines role hierarchy.

Key Fields:

* id
* role_name

Supported Values:

* Field Executive
* Marketing Executive
* Sales Executive
* Manager
* CEO
* Administrator

---

## attendance_logs

Purpose:

Maintains attendance records.

Key Fields:

* id
* user_id
* check_in_time
* latitude
* longitude
* mock_location_detected
* route_summary
* created_at

Relationships:

* Belongs to users.

---

## sites

Purpose:

Represents discovered construction opportunities.

Key Fields:

* id
* site_name
* address
* city
* latitude
* longitude
* project_type
* project_size
* estimated_requirement
* discovered_by
* created_at

Relationships:

* Has many contacts.
* Has many meetings.
* Has many opportunities.

---

## contacts

Purpose:

Stores stakeholders associated with sites.

Key Fields:

* id
* site_id
* name
* contact_type
* mobile_number
* alternate_number
* firm_name
* address
* remarks

Supported Contact Types:

* Owner
* Architect
* Builder
* Referral

Relationships:

* Belongs to sites.

---

## site_media

Purpose:

Stores supporting evidence.

Key Fields:

* id
* site_id
* media_type
* file_url
* uploaded_by
* uploaded_at

Relationships:

* Belongs to sites.

---

## meetings

Purpose:

Tracks marketing interactions.

Key Fields:

* id
* site_id
* conducted_by
* meeting_date
* stakeholder_name
* summary
* follow_up_date
* remarks

Relationships:

* Belongs to sites.
* Belongs to users.

---

## assignments

Purpose:

Tracks responsibility allocation.

Key Fields:

* id
* site_id
* assigned_to
* assigned_by
* assignment_type
* assigned_at

Supported Assignment Types:

* Marketing
* Sales

Relationships:

* Belongs to sites.
* Belongs to users.

---

## showroom_visits

Purpose:

Tracks showroom activities.

Key Fields:

* id
* site_id
* sales_executive_id
* visit_date
* selected_material
* estimated_quantity
* quotation_required
* expected_purchase_date
* remarks

Relationships:

* Belongs to sites.
* Belongs to users.

---

## opportunities

Purpose:

Represents sales opportunities.

Key Fields:

* id
* site_id
* expected_revenue
* quotation_value
* probability_of_conversion
* current_status
* follow_up_date
* remarks

Relationships:

* Belongs to sites.
* Has many lifecycle_history records.
* Has one ownership_record.

---

## lifecycle_history

Purpose:

Maintains lifecycle progression history.

Key Fields:

* id
* opportunity_id
* previous_status
* new_status
* changed_by
* changed_at

Relationships:

* Belongs to opportunities.
* Belongs to users.

---

## ownership_records

Purpose:

Preserves accountability.

Key Fields:

* id
* opportunity_id
* lead_creator_id
* marketing_owner_id
* sales_owner_id
* revenue_credit

Relationships:

* Belongs to opportunities.
* References users.

---

## architect_profiles

Purpose:

Supports architect intelligence.

Key Fields:

* id
* contact_id
* influence_score
* loyalty_score
* project_potential_score
* preferences
* revenue_contribution

Relationships:

* Belongs to contacts.

---

## builder_profiles

Purpose:

Supports builder intelligence.

Key Fields:

* id
* contact_id
* project_volume
* business_potential
* consumption_potential
* future_requirements

Relationships:

* Belongs to contacts.

---

## training_programs

Purpose:

Stores LMS programs.

Key Fields:

* id
* title
* description
* created_by
* created_at

Relationships:

* Has many training_progress records.

---

## training_progress

Purpose:

Tracks employee learning.

Key Fields:

* id
* user_id
* training_program_id
* completion_status
* assessment_score
* certification_status

Relationships:

* Belongs to users.
* Belongs to training_programs.

---

## dashboard_snapshots

Purpose:

Supports reporting optimization.

Key Fields:

* id
* snapshot_date
* attendance_count
* active_opportunities
* confirmed_orders
* revenue_pipeline

---

## audit_logs

Purpose:

Maintains traceability.

Key Fields:

* id
* user_id
* entity_type
* entity_id
* action
* previous_value
* new_value
* created_at

Relationships:

* Belongs to users.

---

## notifications

Purpose:

Supports communication.

Key Fields:

* id
* recipient_id
* title
* message
* is_read
* created_at

Relationships:

* Belongs to users.

---

# 5. Relationship Summary

users
↓
attendance_logs

users
↓
sites

sites
↓
contacts

sites
↓
meetings

sites
↓
assignments

sites
↓
showroom_visits

sites
↓
opportunities

opportunities
↓
lifecycle_history

opportunities
↓
ownership_records

contacts
↓
architect_profiles

contacts
↓
builder_profiles

training_programs
↓
training_progress

users
↓
audit_logs

users
↓
notifications

---

# 6. Indexing Strategy

Recommended Indexes:

* users.mobile_number
* contacts.mobile_number
* sites.city
* opportunities.current_status
* lifecycle_history.opportunity_id
* assignments.assigned_to
* audit_logs.entity_type, entity_id

---

# 7. Search Strategy

Mobile Number shall function as the primary search key.

Search shall retrieve:

* Contact Information
* Site History
* Meetings
* Showroom Visits
* Opportunity Status
* Ownership Information

---

# 8. Audit Strategy

The following actions shall generate audit records:

* Site creation.
* Opportunity updates.
* Lifecycle transitions.
* Assignment changes.
* Ownership changes.
* User administration activities.

---

# 9. Future Expansion

The database supports future implementation of:

* AI forecasting.
* Route optimization.
* Advanced dashboards.
* External integrations.
* Predictive opportunity scoring.

---

# 10. Database Statistics

| Category            | Count |
| ------------------- | ----- |
| Core Tables         | 18    |
| Relationship Tables | 4     |
| Audit Tables        | 1     |
| Reporting Tables    | 1     |

Estimated Initial Total:

18–20 tables.

---

# End of Document
