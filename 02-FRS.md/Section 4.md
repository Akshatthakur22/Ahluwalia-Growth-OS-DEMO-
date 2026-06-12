# 02-FRS.md

# Section 4: Showroom Sales Module Requirements

---

# Module Name

Showroom Sales Module

---

# Module Purpose

The Showroom Sales Module shall enable sales personnel to manage showroom visitors, capture customer requirements, track material selection activities, maintain follow-up schedules, and monitor opportunities through the sales process.

The module shall support structured lead qualification and conversion activities while preserving customer interaction history for future reference.

---

# Functional Requirements

## FR-SRM-001

**Requirement Name:** Showroom Visit Record Creation

**Description:**

The system shall allow sales personnel to create showroom visit records.

---

## FR-SRM-002

**Requirement Name:** Visit Date Capture

**Description:**

The system shall allow sales personnel to record the date of the showroom visit.

---

## FR-SRM-003

**Requirement Name:** Client Name Capture

**Description:**

The system shall allow sales personnel to record the client's name.

---

## FR-SRM-004

**Requirement Name:** Client Contact Number Capture

**Description:**

The system shall allow sales personnel to record the client's contact number.

---

## FR-SRM-005

**Requirement Name:** Client Address Capture

**Description:**

The system shall allow sales personnel to record the client's address.

---

## FR-SRM-006

**Requirement Name:** Area Capture

**Description:**

The system shall allow sales personnel to record the area associated with the client.

---

## FR-SRM-007

**Requirement Name:** City Capture

**Description:**

The system shall allow sales personnel to record the city associated with the client.

---

## FR-SRM-008

**Requirement Name:** Project Type Capture

**Description:**

The system shall allow sales personnel to record the project type associated with the client.

---

## FR-SRM-009

**Requirement Name:** Project Size Capture

**Description:**

The system shall allow sales personnel to record the project size in square feet (SFT).

---

## FR-SRM-010

**Requirement Name:** Architect Information Capture

**Description:**

The system shall allow sales personnel to record architect information associated with the opportunity.

---

## FR-SRM-011

**Requirement Name:** Builder Information Capture

**Description:**

The system shall allow sales personnel to record builder information associated with the opportunity.

---

## FR-SRM-012

**Requirement Name:** Selected Material Capture

**Description:**

The system shall allow sales personnel to record the materials selected by the client.

---

## FR-SRM-013

**Requirement Name:** Quantity Requirement Capture

**Description:**

The system shall allow sales personnel to record the quantity required in square feet (SFT).

---

## FR-SRM-014

**Requirement Name:** Lead Temperature Classification

**Description:**

The system shall support classification of leads using the following categories:

* Cold
* Warm
* Hot

---

## FR-SRM-015

**Requirement Name:** Lead Source Classification

**Description:**

The system shall support classification of lead sources using the following categories:

* Walk-in
* Referral
* Lead
* Personal

---

## FR-SRM-016

**Requirement Name:** Referral Name Capture

**Description:**

The system shall allow sales personnel to record the referral name associated with the opportunity.

---

## FR-SRM-017

**Requirement Name:** Referral Contact Capture

**Description:**

The system shall allow sales personnel to record the referral contact information associated with the opportunity.

---

## FR-SRM-018

**Requirement Name:** Meeting Duration Capture

**Description:**

The system shall allow sales personnel to record the amount of time spent with the client.

---

## FR-SRM-019

**Requirement Name:** Presentation Sharing Status Capture

**Description:**

The system shall allow sales personnel to record whether a presentation has been shared with the client.

The following values shall be supported:

* Yes
* No

---

## FR-SRM-020

**Requirement Name:** 3D Video Sharing Status Capture

**Description:**

The system shall allow sales personnel to record whether a 3D video has been shared with the client.

The following values shall be supported:

* Yes
* No

---

## FR-SRM-021

**Requirement Name:** Quotation Requirement Capture

**Description:**

The system shall allow sales personnel to record whether a quotation is required.

The following values shall be supported:

* Yes
* No

---

## FR-SRM-022

**Requirement Name:** Expected Purchase Timeline Capture

**Description:**

The system shall allow sales personnel to record the expected purchase timeline.

---

## FR-SRM-023

**Requirement Name:** Follow-Up Date Capture

**Description:**

The system shall allow sales personnel to record the next follow-up date.

---

## FR-SRM-024

**Requirement Name:** Remarks Capture

**Description:**

The system shall allow sales personnel to record remarks associated with the showroom interaction.

---

# Inputs

The module shall support capture of the following inputs:

* Visit Date
* Client Name
* Contact Number
* Address
* Area
* City
* Project Type
* Project Size (SFT)
* Architect Name
* Builder Name
* Selected Material
* Quantity Required (SFT)
* Lead Temperature
* Lead Source
* Referral Name
* Referral Contact
* Time Spent
* Presentation Shared
* 3D Video Shared
* Quotation Required
* Expected Purchase Timeline
* Follow-up Date
* Remarks

---

# Outputs

The module shall generate the following outputs:

* Showroom visit records
* Customer interaction history
* Material selection information
* Lead qualification information
* Follow-up schedules
* Sales opportunity records

---

# Stakeholders

| Stakeholder     | Role                   |
| --------------- | ---------------------- |
| Sales Executive | Opportunity Management |
| Management      | Performance Monitoring |
| Marketing Team  | Lead Transfer Provider |

---

# Business Objectives Supported

The Showroom Sales Module supports the following objectives:

* Improve customer engagement.
* Increase conversion rates.
* Standardize showroom sales processes.
* Preserve customer interaction history.
* Support structured follow-up activities.

---

# Constraints

The following constraints have been explicitly identified:

* Lead temperatures shall be limited to Cold, Warm, and Hot.
* Lead sources shall be limited to Walk-in, Referral, Lead, and Personal.
* Presentation sharing status shall be limited to Yes or No.
* 3D video sharing status shall be limited to Yes or No.
* Quotation requirement status shall be limited to Yes or No.

---

# Open Questions

The following items require stakeholder clarification:

1. What values are valid for project type?
2. Can multiple materials be associated with a single showroom visit?
3. Can multiple quotations be generated for a single opportunity?
4. Is referral information mandatory when the lead source is Referral?
5. Should follow-up reminders be generated automatically?
6. Can showroom visits be linked to existing sites discovered by field executives?
7. Should sales personnel be allowed to edit historical showroom records?

---

# Out of Scope (Current Requirement Set)

The following items are not specified within the business requirements document:

* Quotation generation workflows.
* Inventory availability checks.
* Payment collection processes.
* Order fulfillment management.
* Integration with ERP systems.
* Customer notification mechanisms.
* Digital signature capabilities.

---

# Requirement Traceability

| Business Requirement       | Functional Requirement |
| -------------------------- | ---------------------- |
| Visit Date                 | FR-SRM-002             |
| Client Name                | FR-SRM-003             |
| Contact Number             | FR-SRM-004             |
| Address                    | FR-SRM-005             |
| Area                       | FR-SRM-006             |
| City                       | FR-SRM-007             |
| Project Type               | FR-SRM-008             |
| Project Size               | FR-SRM-009             |
| Architect Name             | FR-SRM-010             |
| Builder Name               | FR-SRM-011             |
| Selected Material          | FR-SRM-012             |
| Quantity Required          | FR-SRM-013             |
| Lead Temperature           | FR-SRM-014             |
| Lead Source                | FR-SRM-015             |
| Referral Name              | FR-SRM-016             |
| Referral Contact           | FR-SRM-017             |
| Time Spent                 | FR-SRM-018             |
| Presentation Shared        | FR-SRM-019             |
| 3D Video Shared            | FR-SRM-020             |
| Quotation Required         | FR-SRM-021             |
| Expected Purchase Timeline | FR-SRM-022             |
| Follow-up Date             | FR-SRM-023             |
| Remarks                    | FR-SRM-024             |

---

# End of Section

This section defines the functional requirements associated with the Showroom Sales Module of Ahluwalia Growth OS. These requirements have been derived directly from the business requirements documentation and shall serve as the basis for future design and implementation activities.
