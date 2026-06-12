# 02-FRS.md

# Section 2: Field Executive Module Requirements

---

# Module Name

Field Executive Module

---

# Module Purpose

The Field Executive Module shall enable field executives to capture and maintain detailed information regarding construction sites, project stakeholders, market intelligence, and purchase opportunities encountered during field visits.

The information collected through this module shall contribute to the organization's long-term market intelligence repository and support future marketing and sales activities.

---

# Functional Requirements

## FR-FLD-001

**Requirement Name:** Site Record Creation

**Description:**

The system shall allow field executives to create a site record.

---

## FR-FLD-002

**Requirement Name:** Site Name Capture

**Description:**

The system shall allow field executives to record the site name.

---

## FR-FLD-003

**Requirement Name:** Site Address Capture

**Description:**

The system shall allow field executives to record the site address.

---

## FR-FLD-004

**Requirement Name:** GPS Location Capture

**Description:**

The system shall automatically capture GPS coordinates associated with the site.

---

## FR-FLD-005

**Requirement Name:** City Information Capture

**Description:**

The system shall allow field executives to record the city associated with the site.

---

## FR-FLD-006

**Requirement Name:** Area or Locality Capture

**Description:**

The system shall allow field executives to record the area or locality associated with the site.

---

## FR-FLD-007

**Requirement Name:** Owner Information Capture

**Description:**

The system shall allow field executives to capture owner details, including owner name, contact information, and address.

---

## FR-FLD-008

**Requirement Name:** Builder Information Capture

**Description:**

The system shall allow field executives to capture builder details, including builder name, firm name, contact information, and category.

---

## FR-FLD-009

**Requirement Name:** Builder Category Classification

**Description:**

The system shall support classification of builders using the following categories:

* Category A
* Category B
* Category C
* Category D

---

## FR-FLD-010

**Requirement Name:** Architect Information Capture

**Description:**

The system shall allow field executives to capture architect details, including architect name, firm name, contact information, and category.

---

## FR-FLD-011

**Requirement Name:** Architect Category Classification

**Description:**

The system shall support classification of architects using the following categories:

* Category A
* Category B
* Category C
* Category D

---

## FR-FLD-012

**Requirement Name:** Project Size Capture

**Description:**

The system shall allow field executives to record the estimated project size in square feet (SFT).

---

## FR-FLD-013

**Requirement Name:** Project Stage Capture

**Description:**

The system shall allow field executives to record the project stage using one of the following values:

* 10 Days
* 30 Days
* 50 Days
* 70 Days
* 100 Days

---

## FR-FLD-014

**Requirement Name:** Decision Maker Identification

**Description:**

The system shall allow field executives to record the decision maker associated with the project.

---

## FR-FLD-015

**Requirement Name:** Expected Purchase Timeline Capture

**Description:**

The system shall allow field executives to record the expected purchase timeline.

---

## FR-FLD-016

**Requirement Name:** Current Vendor Information Capture

**Description:**

The system shall allow field executives to record information regarding the current vendor associated with the project.

---

## FR-FLD-017

**Requirement Name:** Material Information Capture

**Description:**

The system shall allow field executives to record information regarding materials currently being used within the project.

---

## FR-FLD-018

**Requirement Name:** Purchase Rate Capture

**Description:**

The system shall allow field executives to record the purchase rate associated with the materials.

---

## FR-FLD-019

**Requirement Name:** Competitor Information Capture

**Description:**

The system shall allow field executives to record competitor information associated with the project.

---

## FR-FLD-020

**Requirement Name:** Geo-Tagged Site Photograph Capture

**Description:**

The system shall allow field executives to upload geo-tagged photographs related to the site.

---

## FR-FLD-021

**Requirement Name:** Remarks Capture

**Description:**

The system shall allow field executives to record remarks associated with the site visit.

---

# Inputs

The module shall support capture of the following inputs:

* Site Name
* Site Address
* GPS Coordinates
* City
* Area/Locality
* Owner Name
* Owner Contact
* Owner Address
* Builder Name
* Builder Firm Name
* Builder Contact
* Builder Category
* Architect Name
* Architect Firm Name
* Architect Contact
* Architect Category
* Project Size (SFT)
* Project Stage
* Decision Maker
* Expected Purchase Timeline
* Current Vendor
* Material Used
* Purchase Rate
* Competitor Name
* Site Photograph
* Remarks

---

# Outputs

The module shall generate the following outputs:

* Site records
* Stakeholder records
* Project intelligence information
* Competitor intelligence information
* Geo-tagged evidence of site visits
* Market intelligence repository entries

---

# Stakeholders

| Stakeholder     | Role                    |
| --------------- | ----------------------- |
| Field Executive | Data Collection         |
| Marketing Team  | Opportunity Development |
| Management      | Oversight and Reporting |

---

# Business Objectives Supported

The Field Executive Module supports the following objectives:

* Development of a permanent market intelligence database.
* Reduction of dependency on employee memory.
* Early identification of sales opportunities.
* Improved coordination between field, marketing, and sales teams.

---

# Constraints

The following constraints have been explicitly identified:

* GPS location shall be captured automatically.
* Site photographs shall be geo-tagged.
* Builder classification shall use categories A, B, C, and D.
* Architect classification shall use categories A, B, C, and D.
* Project stages shall be limited to 10, 30, 50, 70, and 100 days.

---

# Open Questions

The following items require stakeholder clarification:

1. Can multiple builders be associated with a single site?
2. Can multiple architects be associated with a single site?
3. Can multiple photographs be uploaded for a site?
4. Should field executives be allowed to edit previously submitted site records?
5. Should site records support version history?
6. Are project stages mandatory fields?
7. How should duplicate sites be identified?

---

# Out of Scope (Current Requirement Set)

The following items are not specified within the business requirements document:

* Site approval workflows.
* Duplicate detection mechanisms.
* Offline data capture capabilities.
* Automated competitor analysis.
* Integration with external GIS systems.
* Notification mechanisms.

---

# Requirement Traceability

| Business Requirement       | Functional Requirement |
| -------------------------- | ---------------------- |
| Site Name                  | FR-FLD-002             |
| Site Address               | FR-FLD-003             |
| GPS Location (Auto)        | FR-FLD-004             |
| City                       | FR-FLD-005             |
| Area/Locality              | FR-FLD-006             |
| Owner Details              | FR-FLD-007             |
| Builder Details            | FR-FLD-008, FR-FLD-009 |
| Architect Details          | FR-FLD-010, FR-FLD-011 |
| Project Size               | FR-FLD-012             |
| Project Stage              | FR-FLD-013             |
| Decision Maker             | FR-FLD-014             |
| Expected Purchase Timeline | FR-FLD-015             |
| Current Vendor             | FR-FLD-016             |
| Material Used              | FR-FLD-017             |
| Purchase Rate              | FR-FLD-018             |
| Competitor Name            | FR-FLD-019             |
| Site Photo (Geo-tagged)    | FR-FLD-020             |
| Remarks                    | FR-FLD-021             |

---

# End of Section

This section defines the functional requirements associated with the Field Executive Module of Ahluwalia Growth OS. These requirements have been derived directly from the business requirements documentation and shall serve as the basis for future design and implementation activities.
