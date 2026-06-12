# 02-FRS.md

# Section 7: Showroom Visit Request Module Requirements

---

# Module Name

Showroom Visit Request Module

---

# Module Purpose

The Showroom Visit Request Module shall enable marketing executives to formally transfer qualified opportunities to the sales function once a showroom visit commitment has been secured from the builder or architect.

The module shall establish a structured lead handover process between marketing and sales teams while preserving opportunity context and ownership information.

---

# Functional Requirements

## FR-SVR-001

**Requirement Name:** Lead Transfer Request Creation

**Description:**

The system shall allow marketing executives to create lead transfer requests.

---

## FR-SVR-002

**Requirement Name:** Showroom Visit Commitment Validation

**Description:**

The system shall support creation of lead transfer requests when a builder or architect has agreed to visit the showroom.

---

## FR-SVR-003

**Requirement Name:** Site Association

**Description:**

The system shall allow lead transfer requests to be associated with a specific Site ID.

---

## FR-SVR-004

**Requirement Name:** Builder Information Association

**Description:**

The system shall allow builder information to be associated with the lead transfer request.

---

## FR-SVR-005

**Requirement Name:** Architect Information Association

**Description:**

The system shall allow architect information to be associated with the lead transfer request.

---

## FR-SVR-006

**Requirement Name:** Expected Visit Date Capture

**Description:**

The system shall allow marketing executives to record the expected showroom visit date.

---

## FR-SVR-007

**Requirement Name:** Expected Quantity Capture

**Description:**

The system shall allow marketing executives to record the expected quantity requirement in square feet (SFT).

---

## FR-SVR-008

**Requirement Name:** Priority Classification

**Description:**

The system shall support classification of lead transfer requests using the following priority levels:

* High
* Medium
* Low

---

## FR-SVR-009

**Requirement Name:** Transfer Remarks Capture

**Description:**

The system shall allow marketing executives to record remarks associated with the lead transfer request.

---

## FR-SVR-010

**Requirement Name:** Lead Transfer Record Maintenance

**Description:**

The system shall maintain records of lead transfer requests created by marketing executives.

---

# Inputs

The module shall support capture of the following inputs:

* Site ID
* Builder Name
* Architect Name
* Expected Visit Date
* Expected Quantity (SFT)
* Priority
* Remarks

---

# Outputs

The module shall generate the following outputs:

* Lead transfer records
* Showroom visit requests
* Sales handover information
* Opportunity prioritization information
* Transfer history records

---

# Stakeholders

| Stakeholder         | Role                    |
| ------------------- | ----------------------- |
| Marketing Executive | Lead Transfer Initiator |
| Sales Executive     | Future Lead Recipient   |
| Manager             | Oversight Authority     |
| CEO                 | Executive Visibility    |

---

# Business Objectives Supported

The Showroom Visit Request Module supports the following objectives:

* Improve coordination between marketing and sales teams.
* Ensure structured opportunity handover.
* Preserve opportunity context during ownership transitions.
* Improve showroom preparedness.
* Strengthen accountability across functions.

---

# Constraints

The following constraints have been explicitly identified:

* Lead transfer requests shall originate from marketing executives.
* Lead transfer requests shall be associated with a Site ID.
* Expected quantities shall be captured in SFT.
* Priority classifications shall be limited to:

  * High
  * Medium
  * Low.
* Transfer requests shall involve builders and/or architects who have agreed to showroom visits.

---

# Open Questions

The following items require stakeholder clarification:

1. Can showroom visit requests be created without both builder and architect information?
2. Can multiple showroom visit requests exist for the same site?
3. Can expected visit dates be modified after request creation?
4. Should transfer requests expire if the showroom visit does not occur?
5. Should managers approve lead transfer requests before they reach sales?
6. Can marketing executives cancel previously submitted requests?
7. Should notifications be generated for sales teams upon request creation?

---

# Out of Scope (Current Requirement Set)

The following items are not specified within the business requirements document:

* Transfer approval workflows.
* Automated notifications.
* Calendar integrations.
* Showroom scheduling mechanisms.
* Visit rescheduling processes.
* Reminder systems.
* Transfer rejection workflows.

---

# Requirement Traceability

| Business Requirement                              | Functional Requirement |
| ------------------------------------------------- | ---------------------- |
| Marketing Executive creates lead transfer request | FR-SVR-001             |
| Builder/architect agrees to visit showroom        | FR-SVR-002             |
| Site ID                                           | FR-SVR-003             |
| Builder Name                                      | FR-SVR-004             |
| Architect Name                                    | FR-SVR-005             |
| Expected Visit Date                               | FR-SVR-006             |
| Expected Quantity (SFT)                           | FR-SVR-007             |
| Priority                                          | FR-SVR-008             |
| Remarks                                           | FR-SVR-009             |
| Lead transfer request record                      | FR-SVR-010             |

---

# End of Section

This section defines the functional requirements associated with the Showroom Visit Request Module of Ahluwalia Growth OS. These requirements have been derived directly from the business requirements documentation and establish the formal transition of qualified opportunities from marketing ownership to the sales process.
