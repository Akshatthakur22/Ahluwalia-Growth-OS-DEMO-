# 02-FRS.md

# Section 3: Marketing Team Module Requirements

---

# Module Name

Marketing Team Module

---

# Module Purpose

The Marketing Team Module shall enable marketing personnel to record stakeholder interactions, assess relationship quality, identify business opportunities, and systematically manage follow-up activities.

The module shall support structured relationship-building efforts with architects, builders, owners, and designers while ensuring that engagement history becomes a permanent organizational asset.

---

# Functional Requirements

## FR-MKT-001

**Requirement Name:** Meeting Record Creation

**Description:**

The system shall allow marketing team members to create meeting records.

---

## FR-MKT-002

**Requirement Name:** Meeting Date Capture

**Description:**

The system shall allow marketing team members to record the meeting date.

---

## FR-MKT-003

**Requirement Name:** Meeting Time Capture

**Description:**

The system shall allow marketing team members to record the meeting time.

---

## FR-MKT-004

**Requirement Name:** Meeting Participant Classification

**Description:**

The system shall allow marketing team members to classify the person met using one of the following categories:

* Owner
* Builder
* Architect
* Designer

---

## FR-MKT-005

**Requirement Name:** Person Name Capture

**Description:**

The system shall allow marketing team members to record the name of the person met.

---

## FR-MKT-006

**Requirement Name:** Contact Number Capture

**Description:**

The system shall allow marketing team members to record the contact number of the person met.

---

## FR-MKT-007

**Requirement Name:** Firm Name Capture

**Description:**

The system shall allow marketing team members to record the associated firm name.

---

## FR-MKT-008

**Requirement Name:** Address Capture

**Description:**

The system shall allow marketing team members to record the address associated with the meeting participant.

---

## FR-MKT-009

**Requirement Name:** Area Capture

**Description:**

The system shall allow marketing team members to record the area associated with the meeting participant.

---

## FR-MKT-010

**Requirement Name:** City Capture

**Description:**

The system shall allow marketing team members to record the city associated with the meeting participant.

---

## FR-MKT-011

**Requirement Name:** Participant Category Classification

**Description:**

The system shall support categorization of meeting participants using the following categories:

* Category A
* Category B
* Category C
* Category D

---

## FR-MKT-012

**Requirement Name:** Relationship Stage Capture

**Description:**

The system shall allow marketing team members to record the relationship stage associated with the meeting participant.

---

## FR-MKT-013

**Requirement Name:** Influence Score Capture

**Description:**

The system shall allow marketing team members to assign an influence score ranging from 1 to 10.

---

## FR-MKT-014

**Requirement Name:** Opportunity Score Capture

**Description:**

The system shall allow marketing team members to assign an opportunity score ranging from 1 to 10.

---

## FR-MKT-015

**Requirement Name:** Loyalty Score Capture

**Description:**

The system shall allow marketing team members to assign a loyalty score ranging from 1 to 10.

---

## FR-MKT-016

**Requirement Name:** Meeting Duration Capture

**Description:**

The system shall allow marketing team members to record the amount of time spent during the meeting.

---

## FR-MKT-017

**Requirement Name:** Current Requirement Capture

**Description:**

The system shall allow marketing team members to record the current requirement discussed during the meeting.

---

## FR-MKT-018

**Requirement Name:** Estimated Project Size Capture

**Description:**

The system shall allow marketing team members to record the estimated project size in square feet (SFT).

---

## FR-MKT-019

**Requirement Name:** Showroom Visit Commitment Capture

**Description:**

The system shall allow marketing team members to record whether a showroom visit commitment has been obtained.

The following values shall be supported:

* Yes
* No

---

## FR-MKT-020

**Requirement Name:** Follow-Up Date Capture

**Description:**

The system shall allow marketing team members to record the next follow-up date.

---

## FR-MKT-021

**Requirement Name:** Meeting Remarks Capture

**Description:**

The system shall allow marketing team members to record remarks related to the meeting.

---

## FR-MKT-022

**Requirement Name:** Automatic Location Capture

**Description:**

The system shall automatically capture GPS location information associated with the meeting.

---

# Inputs

The module shall support capture of the following inputs:

* Meeting Date
* Meeting Time
* Participant Type
* Person Name
* Contact Number
* Firm Name
* Address
* Area
* City
* Category
* Relationship Stage
* Influence Score
* Opportunity Score
* Loyalty Score
* Time Spent
* Current Requirement
* Estimated Project Size
* Showroom Visit Commitment
* Next Follow-up Date
* Meeting Remarks
* GPS Location

---

# Outputs

The module shall generate the following outputs:

* Meeting records
* Relationship intelligence records
* Opportunity evaluation data
* Follow-up schedules
* Stakeholder engagement history
* GPS-backed meeting evidence

---

# Stakeholders

| Stakeholder         | Role                          |
| ------------------- | ----------------------------- |
| Marketing Executive | Relationship Management       |
| Management          | Performance Monitoring        |
| Sales Team          | Opportunity Handover Consumer |

---

# Business Objectives Supported

The Marketing Team Module supports the following objectives:

* Improve relationship management.
* Increase follow-up discipline.
* Enhance opportunity identification.
* Preserve engagement history.
* Support future revenue generation.

---

# Constraints

The following constraints have been explicitly identified:

* Participant type shall be limited to Owner, Builder, Architect, or Designer.
* Categories shall be limited to A, B, C, and D.
* Influence scores shall range from 1 to 10.
* Opportunity scores shall range from 1 to 10.
* Loyalty scores shall range from 1 to 10.
* Showroom visit commitment shall be limited to Yes or No.
* GPS location shall be captured automatically.

---

# Open Questions

The following items require stakeholder clarification:

1. What values are valid for relationship stages?
2. Can multiple participants be associated with a single meeting?
3. Can a meeting be linked to an existing site?
4. Should supporting documents or attachments be allowed?
5. Can follow-up dates be modified after creation?
6. Should reminders be generated for upcoming follow-ups?
7. How should missed follow-ups be handled?

---

# Out of Scope (Current Requirement Set)

The following items are not specified within the business requirements document:

* Automated follow-up notifications.
* Calendar integrations.
* Email integrations.
* Meeting approval workflows.
* Voice recording capabilities.
* Attachment management.
* Meeting rescheduling workflows.

---

# Requirement Traceability

| Business Requirement         | Functional Requirement |
| ---------------------------- | ---------------------- |
| Meeting Date                 | FR-MKT-002             |
| Meeting Time                 | FR-MKT-003             |
| Met With                     | FR-MKT-004             |
| Person Name                  | FR-MKT-005             |
| Contact Number               | FR-MKT-006             |
| Firm Name                    | FR-MKT-007             |
| Address                      | FR-MKT-008             |
| Area                         | FR-MKT-009             |
| City                         | FR-MKT-010             |
| Category                     | FR-MKT-011             |
| Relationship Stage           | FR-MKT-012             |
| Influence Score              | FR-MKT-013             |
| Opportunity Score            | FR-MKT-014             |
| Loyalty Score                | FR-MKT-015             |
| Time Spent                   | FR-MKT-016             |
| Current Requirement          | FR-MKT-017             |
| Estimated Project Size       | FR-MKT-018             |
| Showroom Visit Commitment    | FR-MKT-019             |
| Next Follow-up Date          | FR-MKT-020             |
| Meeting Remarks              | FR-MKT-021             |
| Location Captured (Auto GPS) | FR-MKT-022             |

---

# End of Section

This section defines the functional requirements associated with the Marketing Team Module of Ahluwalia Growth OS. These requirements have been derived directly from the business requirements documentation and shall serve as the basis for subsequent design and implementation activities.
