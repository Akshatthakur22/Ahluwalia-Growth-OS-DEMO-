# 03-Data-Dictionary.md

## Document Information

| Item          | Value                      |
| ------------- | -------------------------- |
| Document Name | Data Dictionary            |
| System        | Ahluwalia Growth OS        |
| Version       | 1.0                        |
| Status        | Draft                      |
| Prepared By   | Product & Engineering Team |
| Based On      | BRD v1.0, FRS v1.0         |

---

# 1. Introduction

## Purpose

This document defines the business entities and data elements used within Ahluwalia Growth OS.

The objective is to provide a single source of truth for developers, product stakeholders, designers, and AI-assisted implementation tools.

The document focuses on **implementation-ready business data definitions** while avoiding unnecessary technical details that will be covered within database design documentation.

---

# 2. Entity Overview

The following entities constitute the core data model of Ahluwalia Growth OS.

| Entity            |
| ----------------- |
| User              |
| Attendance        |
| Site              |
| Contact           |
| Meeting           |
| Assignment        |
| Showroom Visit    |
| Opportunity       |
| Lifecycle         |
| Ownership         |
| Architect         |
| Builder           |
| LMS               |
| Dashboard Metrics |

---

# 3. User Entity

Purpose:
Represents every individual interacting with Growth OS.

Fields:

* Employee ID
* Employee Name
* Mobile Number
* Email Address
* Role
* Department
* Reporting Manager
* Employment Status
* Date of Joining
* Assigned Region

---

# 4. Attendance Entity

Purpose:
Captures attendance and live tracking information.

Fields:

* Employee
* Login Time
* GPS Location
* Mock Location Status
* Attendance Status
* Route Information
* Productivity Metrics

---

# 5. Site Entity

Purpose:
Represents construction sites discovered by field teams.

Fields:

* Site Name
* Site Address
* Area
* City
* GPS Coordinates
* Site Stage
* Project Type
* Project Size (SFT)
* Estimated Requirement
* Competitor Brand
* Competitor Quantity
* Site Remarks

---

# 6. Contact Entity

Purpose:
Stores stakeholder information associated with sites.

Fields:

* Contact Name
* Contact Type
* Mobile Number
* Alternate Number
* Address
* Firm Name
* Designation
* Associated Site

Supported Contact Types:

* Owner
* Builder
* Architect
* Referral

---

# 7. Meeting Entity

Purpose:
Captures interactions conducted by marketing teams.

Fields:

* Meeting Date
* Meeting Type
* Stakeholder
* Discussion Summary
* Next Follow-Up Date
* Relationship Score
* Meeting Remarks

---

# 8. Assignment Entity

Purpose:
Tracks ownership assignments.

Fields:

* Site
* Assigned Employee
* Assignment Type
* Assigned By
* Assignment Date
* Priority
* Target Follow-Up Date
* Remarks

Supported Assignment Types:

* Marketing Assignment
* Sales Assignment

---

# 9. Showroom Visit Entity

Purpose:
Tracks showroom-related activities.

Fields:

* Visit Date
* Client Name
* Contact Number
* Project Type
* Project Size
* Selected Material
* Quantity Required
* Lead Temperature
* Lead Source
* Presentation Shared
* 3D Video Shared
* Quotation Required
* Expected Purchase Timeline
* Follow-Up Date
* Remarks

---

# 10. Opportunity Entity

Purpose:
Represents sales opportunities progressing through the lifecycle.

Fields:

* Opportunity Name
* Site
* Expected Revenue
* Expected Quantity
* Quotation Value
* Probability of Conversion
* Opportunity Status
* Follow-Up Date
* Remarks

---

# 11. Lifecycle Entity

Purpose:
Defines opportunity progression stages.

Supported Values:

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

# 12. Ownership Entity

Purpose:
Tracks accountability across opportunity lifecycle.

Fields:

* Lead Creator
* Lead Nurturer
* Lead Converter
* Revenue Generated

---

# 13. Architect Entity

Purpose:
Supports architect intelligence and prioritization.

Fields:

* Architect Name
* Influence Score
* Loyalty Score
* Project Potential Score
* Project History
* Preferences
* Revenue Contribution

---

# 14. Builder Entity

Purpose:
Supports builder intelligence and strategic planning.

Fields:

* Builder Name
* Project Volume
* Business Potential
* Ongoing Projects
* Consumption Potential
* Future Requirements

---

# 15. LMS Entity

Purpose:
Tracks employee learning activities.

Fields:

* Training Program
* Employee
* Assessment
* Assessment Result
* Progress Status
* Certification Status

---

# 16. Dashboard Metrics Entity

Purpose:
Defines information displayed within executive dashboards.

Metrics:

* Attendance Trends
* Site Visits
* Meetings Conducted
* Opportunity Pipeline
* Revenue Forecast
* Conversion Rate
* Team Productivity
* Lifecycle Distribution
* Ownership Visibility
* LMS Progress

---

# 17. Business Rules Summary

Key Rules:

* Every opportunity shall maintain lifecycle information.
* Every opportunity shall maintain ownership information.
* Mobile Number shall act as the primary search key.
* Mock GPS locations shall not be accepted for attendance.
* Lifecycle stages shall follow approved workflow transitions.
* Only active employees shall access the system.

---

# 18. Open Questions

Items requiring future clarification:

* Exact scoring mechanisms.
* Dashboard formulas.
* AI forecasting approaches.
* Notification requirements.
* Reassignment policies.
* Revenue attribution edge cases.

---

# End of Document
