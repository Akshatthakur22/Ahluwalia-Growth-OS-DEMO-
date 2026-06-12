# 02-FRS.md

# Section 11: Site Lifecycle Module Requirements

---

# Module Name

Site Lifecycle Module

---

# Module Purpose

The Site Lifecycle Module shall enable the organization to track the progression of opportunities from initial discovery through relationship development, sales execution, and final outcome.

The module shall provide a standardized representation of opportunity stages, improve visibility into pipeline status, and support monitoring of business progression across teams.

---

# Functional Requirements

## FR-LIF-001

**Requirement Name:** Lifecycle Status Management

**Description:**

The system shall maintain lifecycle status information for opportunities managed within the platform.

---

## FR-LIF-002

**Requirement Name:** New Site Status Support

**Description:**

The system shall support the lifecycle status:

* New Site

to represent opportunities that have been newly identified.

---

## FR-LIF-003

**Requirement Name:** Relationship Building Status Support

**Description:**

The system shall support the lifecycle status:

* Relationship Building

to represent opportunities undergoing marketing engagement activities.

---

## FR-LIF-004

**Requirement Name:** Showroom Visit Scheduled Status Support

**Description:**

The system shall support the lifecycle status:

* Showroom Visit Scheduled

to represent opportunities for which showroom visits have been planned.

---

## FR-LIF-005

**Requirement Name:** Showroom Visit Done Status Support

**Description:**

The system shall support the lifecycle status:

* Showroom Visit Done

to represent opportunities where showroom visits have been completed.

---

## FR-LIF-006

**Requirement Name:** Selection Done Status Support

**Description:**

The system shall support the lifecycle status:

* Selection Done

to represent opportunities where material selection activities have been completed.

---

## FR-LIF-007

**Requirement Name:** Quotation Sent Status Support

**Description:**

The system shall support the lifecycle status:

* Quotation Sent

to represent opportunities where quotations have been shared.

---

## FR-LIF-008

**Requirement Name:** Negotiation Status Support

**Description:**

The system shall support the lifecycle status:

* Negotiation

to represent opportunities undergoing negotiation activities.

---

## FR-LIF-009

**Requirement Name:** Order Confirmed Status Support

**Description:**

The system shall support the lifecycle status:

* Order Confirmed

to represent opportunities that have resulted in successful conversions.

---

## FR-LIF-010

**Requirement Name:** Lost Status Support

**Description:**

The system shall support the lifecycle status:

* Lost

to represent opportunities that have not resulted in successful conversions.

---

## FR-LIF-011

**Requirement Name:** Lifecycle Status Association

**Description:**

The system shall maintain lifecycle status information against individual opportunities.

---

## FR-LIF-012

**Requirement Name:** Lifecycle Visibility Support

**Description:**

The system shall provide visibility into the current lifecycle stage associated with opportunities.

---

## FR-LIF-013

**Requirement Name:** Lifecycle Progression Tracking

**Description:**

The system shall maintain records of opportunity progression across lifecycle stages.

---

# Inputs

The module shall support the following lifecycle statuses:

* New Site
* Relationship Building
* Showroom Visit Scheduled
* Showroom Visit Done
* Selection Done
* Quotation Sent
* Negotiation
* Order Confirmed
* Lost

---

# Outputs

The module shall generate the following outputs:

* Opportunity status information
* Pipeline stage information
* Lifecycle progression information
* Opportunity outcome information
* Lifecycle visibility information

---

# Stakeholders

| Stakeholder         | Role                                 |
| ------------------- | ------------------------------------ |
| Field Executive     | Opportunity Discovery Contributor    |
| Marketing Executive | Relationship Development Contributor |
| Sales Executive     | Conversion Contributor               |
| Manager             | Lifecycle Oversight                  |
| CEO                 | Executive Visibility                 |

---

# Business Objectives Supported

The Site Lifecycle Module supports the following objectives:

* Standardize opportunity progression.
* Improve pipeline visibility.
* Strengthen execution discipline.
* Support opportunity monitoring.
* Enable tracking of business outcomes.
* Increase transparency across departments.

---

# Constraints

The following constraints have been explicitly identified:

* Lifecycle statuses shall be limited to:

  * New Site
  * Relationship Building
  * Showroom Visit Scheduled
  * Showroom Visit Done
  * Selection Done
  * Quotation Sent
  * Negotiation
  * Order Confirmed
  * Lost

* Lifecycle information shall be maintained against opportunities.

---

# Open Questions

The following items require stakeholder clarification:

1. Can opportunities move backward between lifecycle stages?
2. Can opportunities skip intermediate stages?
3. Who is authorized to update lifecycle statuses?
4. Should reasons for marking opportunities as Lost be recorded?
5. Can opportunities be reopened after being marked as Lost?
6. Should timestamps be maintained for lifecycle transitions?
7. Should lifecycle transitions generate notifications?

---

# Out of Scope (Current Requirement Set)

The following items are not specified within the business requirements document:

* Automated lifecycle progression rules.
* Approval workflows for stage transitions.
* Lost opportunity categorization.
* Opportunity reopening mechanisms.
* Transition notifications.
* SLA monitoring.
* Pipeline forecasting algorithms.

---

# Requirement Traceability

| Business Requirement     | Functional Requirement |
| ------------------------ | ---------------------- |
| New Site                 | FR-LIF-002             |
| Relationship Building    | FR-LIF-003             |
| Showroom Visit Scheduled | FR-LIF-004             |
| Showroom Visit Done      | FR-LIF-005             |
| Selection Done           | FR-LIF-006             |
| Quotation Sent           | FR-LIF-007             |
| Negotiation              | FR-LIF-008             |
| Order Confirmed          | FR-LIF-009             |
| Lost                     | FR-LIF-010             |
| Lifecycle management     | FR-LIF-001             |
| Lifecycle association    | FR-LIF-011             |
| Lifecycle visibility     | FR-LIF-012             |
| Lifecycle progression    | FR-LIF-013             |

---

# End of Section

This section defines the functional requirements associated with the Site Lifecycle Module of Ahluwalia Growth OS. These requirements have been derived directly from the business requirements documentation and establish the standardized opportunity progression framework used across the organization.
