# 05-State-Transition-Specification.md

# Ahluwalia Growth OS

Version: 1.0

Status: Draft

Prepared By: Product & Engineering Team

Based On: BRD v1.0, FRS v1.0, Client Briefing PDF

---

# 1. Purpose

This document defines the lifecycle states and permitted transitions for opportunities managed within Ahluwalia Growth OS.

The objective is to ensure consistency in opportunity progression, support backend validation rules, enable accurate reporting, and establish a shared understanding of how opportunities evolve throughout their lifecycle.

---

# 2. Transition Classification

Transitions within this document are classified as follows:

| Code | Meaning                                  |
| ---- | ---------------------------------------- |
| P    | Explicitly stated within the client PDF  |
| D    | Derived from approved business workflows |
| Q    | Requires client clarification            |

---

# 3. Lifecycle States

The following lifecycle states have been identified from the client PDF.

| State                    |
| ------------------------ |
| New Site                 |
| Relationship Building    |
| Showroom Visit Scheduled |
| Showroom Visit Done      |
| Selection Done           |
| Quotation Sent           |
| Negotiation              |
| Order Confirmed          |
| Lost                     |

---

# 4. Lifecycle Flow Overview

New Site
↓
Relationship Building
↓
Showroom Visit Scheduled
↓
Showroom Visit Done
↓
Selection Done
↓
Quotation Sent
↓
Negotiation
↓
Order Confirmed

Alternative Outcome:

Any Active State
↓
Lost

---

# 5. State Definitions

## 5.1 New Site

Definition:

Represents a newly discovered opportunity captured by a Field Executive.

Entry Criteria:

* Site information captured.
* Opportunity created within system.

Exit Criteria:

* Opportunity assigned for relationship development.

Owner:

Field Executive.

---

## 5.2 Relationship Building

Definition:

Represents the stage during which Marketing Executives nurture relationships with stakeholders.

Entry Criteria:

* Site assigned to Marketing Executive.

Exit Criteria:

* Showroom visit commitment secured.

Owner:

Marketing Executive.

---

## 5.3 Showroom Visit Scheduled

Definition:

Represents opportunities where stakeholders have agreed to visit the showroom.

Entry Criteria:

* Showroom visit request created.

Exit Criteria:

* Showroom visit completed.

Owner:

Marketing Executive / Sales Executive.

---

## 5.4 Showroom Visit Done

Definition:

Represents opportunities where showroom interactions have occurred.

Entry Criteria:

* Showroom visit completed.

Exit Criteria:

* Material selection completed.

Owner:

Sales Executive.

---

## 5.5 Selection Done

Definition:

Represents opportunities where material selections have been finalized.

Entry Criteria:

* Selected material recorded.

Exit Criteria:

* Quotation prepared and shared.

Owner:

Sales Executive.

---

## 5.6 Quotation Sent

Definition:

Represents opportunities where quotations have been issued.

Entry Criteria:

* Quotation value recorded.
* Quotation shared.

Exit Criteria:

* Negotiation initiated.

Owner:

Sales Executive.

---

## 5.7 Negotiation

Definition:

Represents opportunities undergoing commercial discussions.

Entry Criteria:

* Quotation discussions initiated.

Exit Criteria:

* Order confirmed.
* Opportunity lost.

Owner:

Sales Executive.

---

## 5.8 Order Confirmed

Definition:

Represents successfully converted opportunities.

Entry Criteria:

* Customer acceptance obtained.

Exit Criteria:

None.

Owner:

Sales Executive.

Terminal State:

Yes.

---

## 5.9 Lost

Definition:

Represents opportunities that will no longer be pursued.

Entry Criteria:

* Opportunity closed without conversion.

Exit Criteria:

None.

Owner:

Sales Executive / Management.

Terminal State:

Yes.

---

# 6. Approved Transition Matrix

| From State               | To State                 | Classification |
| ------------------------ | ------------------------ | -------------- |
| New Site                 | Relationship Building    | D              |
| Relationship Building    | Showroom Visit Scheduled | P              |
| Showroom Visit Scheduled | Showroom Visit Done      | D              |
| Showroom Visit Done      | Selection Done           | D              |
| Selection Done           | Quotation Sent           | D              |
| Quotation Sent           | Negotiation              | D              |
| Negotiation              | Order Confirmed          | P              |
| Negotiation              | Lost                     | P              |
| New Site                 | Lost                     | P              |
| Relationship Building    | Lost                     | P              |
| Showroom Visit Scheduled | Lost                     | P              |
| Showroom Visit Done      | Lost                     | P              |
| Selection Done           | Lost                     | P              |
| Quotation Sent           | Lost                     | P              |

---

# 7. Transition Rules

## STR-001

Opportunities shall begin in the "New Site" state.

---

## STR-002

Only one active lifecycle state shall exist for an opportunity at a given time.

---

## STR-003

Transitions shall follow approved pathways defined within this specification.

---

## STR-004

Order Confirmed shall be treated as a terminal state.

---

## STR-005

Lost shall be treated as a terminal state.

---

## STR-006

All lifecycle changes shall be auditable.

---

## STR-007

Lifecycle changes shall update dashboard reporting information.

---

# 8. Role Responsibilities

| State                    | Primary Owner                |
| ------------------------ | ---------------------------- |
| New Site                 | Field Executive              |
| Relationship Building    | Marketing Executive          |
| Showroom Visit Scheduled | Marketing Executive          |
| Showroom Visit Done      | Sales Executive              |
| Selection Done           | Sales Executive              |
| Quotation Sent           | Sales Executive              |
| Negotiation              | Sales Executive              |
| Order Confirmed          | Sales Executive              |
| Lost                     | Sales Executive / Management |

---

# 9. Derived Assumptions

The following items have been derived from approved workflows and are not explicitly stated within the client PDF:

1. Opportunities begin in the New Site state.
2. Showroom Visit Done precedes Selection Done.
3. Selection Done precedes Quotation Sent.
4. Quotation Sent precedes Negotiation.

These assumptions shall be validated with stakeholders during detailed design discussions.

---

# 10. Open Questions

The following items require clarification from Ahluwalia stakeholders:

1. Can opportunities move backwards between states?
2. Can stages be skipped?
3. Can Lost opportunities be reopened?
4. Who is authorized to override transition rules?
5. Should reasons for Lost opportunities be captured?
6. Should timestamps be retained for each transition?
7. Should notifications be triggered during lifecycle changes?

---

# 11. Impact on System Design

This specification shall influence:

* Database validation logic.
* Backend transition rules.
* Frontend action visibility.
* Dashboard calculations.
* Audit logging implementation.
* Claude implementation guidelines.

---

# 12. Transition Diagram (Reference)

New Site
↓
Relationship Building
↓
Showroom Visit Scheduled
↓
Showroom Visit Done
↓
Selection Done
↓
Quotation Sent
↓
Negotiation
↓
Order Confirmed

Alternative Outcome:

Any Active State
↓
Lost

---

# End of Document
