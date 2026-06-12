"""
Seed script to initialize the database with users and sample MVP data.
Run this after configuring your database connection.
"""
import sys
import os
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import (
    User, Role, EmploymentStatus, Site, Contact, Meeting,
    Opportunity, OwnershipRecord, ShowroomVisit, Assignment,
)
from app.models.opportunity import OpportunityStatus
from app.services.auth import AuthService

# Ensure all models are registered before create_all
import app.models  # noqa: F401


def seed_database():
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()
    auth_service = AuthService()

    try:
        if db.query(User).filter(User.role == Role.ADMINISTRATOR).first():
            print("Database already seeded. Skipping.")
            return

        admin = User(
            employee_code="ADMIN001",
            full_name="System Administrator",
            mobile_number="9999999999",
            email="admin@ahluwalia.com",
            hashed_password=auth_service.get_password_hash("admin123"),
            role=Role.ADMINISTRATOR,
            department="IT",
            status=EmploymentStatus.ACTIVE,
            assigned_region="All",
        )
        db.add(admin)

        users_data = [
            ("FE001", "Rohit Sain", "9876543210", Role.FIELD_EXECUTIVE, "Field Operations"),
            ("ME001", "Namita Kaushal", "9876543211", Role.MARKETING_EXECUTIVE, "Marketing"),
            ("SE001", "Rakesh Pandey", "9876543212", Role.SALES_EXECUTIVE, "Showroom Sales"),
            ("MG001", "Vikram Patel", "9876543213", Role.MANAGER, "Management"),
            ("CEO001", "Pritpal Singh", "9876543214", Role.CEO, "Executive"),
        ]
        users = {}
        for code, name, mobile, role, dept in users_data:
            u = User(
                employee_code=code,
                full_name=name,
                mobile_number=mobile,
                hashed_password=auth_service.get_password_hash("password123"),
                role=role,
                department=dept,
                status=EmploymentStatus.ACTIVE,
                assigned_region="North",
            )
            db.add(u)
            users[code] = u

        db.flush()

        fe = users["FE001"]
        me = users["ME001"]
        se = users["SE001"]
        mg = users["MG001"]

        site = Site(
            site_name="Green Valley Residency",
            address="Sector 45, Golf Course Road",
            city="Gurgaon",
            area="Sector 45",
            site_stage="structure",
            project_type="residential",
            discovered_by=fe.id,
            site_remarks="High potential residential project",
        )
        db.add(site)
        db.flush()

        contact = Contact(
            site_id=site.id,
            name="Ravi Mehta",
            contact_type="builder",
            mobile_number="9812345678",
            firm_name="Mehta Constructions",
            designation="Project Manager",
        )
        db.add(contact)

        opportunity = Opportunity(
            site_id=site.id,
            opportunity_name="Green Valley Residency - Opportunity",
            current_status=OpportunityStatus.RELATIONSHIP_BUILDING.value,
            expected_revenue=2500000,
            probability_of_conversion=60,
        )
        db.add(opportunity)
        db.flush()

        db.add(OwnershipRecord(
            opportunity_id=opportunity.id,
            lead_creator_id=fe.id,
            marketing_owner_id=me.id,
        ))

        db.add(Meeting(
            site_id=site.id,
            conducted_by=me.id,
            meeting_date=datetime.now(timezone.utc) - timedelta(days=2),
            meeting_type="site_visit",
            stakeholder_name="Ravi Mehta",
            summary="Discussed marble requirements for lobby and bathrooms",
            follow_up_date=datetime.now(timezone.utc) + timedelta(days=5),
            relationship_score="good",
        ))

        db.add(ShowroomVisit(
            site_id=site.id,
            sales_executive_id=se.id,
            visit_date=datetime.now(timezone.utc) - timedelta(days=1),
            selected_material="Italian Carrara Marble",
            estimated_quantity=500,
            quotation_required=True,
        ))

        db.add(Assignment(
            site_id=site.id,
            assigned_to=me.id,
            assigned_by=mg.id,
            assignment_type="marketing",
            assigned_at=datetime.now(timezone.utc) - timedelta(days=7),
            priority="high",
        ))

        db.commit()
        print("✓ Database seeded successfully")
        print("  Admin: 9999999999 / admin123")
        print("  Sample users: 9876543210-9876543214 / password123")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("Seeding Ahluwalia Growth OS database...")
    seed_database()
