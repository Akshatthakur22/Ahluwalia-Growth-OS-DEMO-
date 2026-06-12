"""
Add PDF-spec columns to existing tables (PostgreSQL).
Safe to run multiple times.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from app.database import engine

COLUMNS = [
    ("contacts", "category", "VARCHAR(10)"),
    ("sites", "decision_maker", "VARCHAR(200)"),
    ("sites", "expected_purchase_timeline", "VARCHAR(200)"),
    ("meetings", "stakeholder_mobile", "VARCHAR(20)"),
    ("meetings", "influence_score", "NUMERIC(4,1)"),
    ("meetings", "opportunity_score", "NUMERIC(4,1)"),
    ("meetings", "loyalty_score", "NUMERIC(4,1)"),
    ("meetings", "showroom_visit_commitment", "BOOLEAN DEFAULT FALSE"),
    ("meetings", "time_spent_minutes", "INTEGER"),
    ("meetings", "current_requirement", "TEXT"),
    ("meetings", "estimated_project_size", "NUMERIC(15,2)"),
    ("meetings", "latitude", "VARCHAR(50)"),
    ("meetings", "longitude", "VARCHAR(50)"),
    ("showroom_visits", "client_name", "VARCHAR(200)"),
    ("showroom_visits", "client_mobile", "VARCHAR(20)"),
    ("showroom_visits", "client_address", "VARCHAR(500)"),
    ("showroom_visits", "client_area", "VARCHAR(100)"),
    ("showroom_visits", "client_city", "VARCHAR(100)"),
    ("showroom_visits", "project_type", "VARCHAR(50)"),
    ("showroom_visits", "project_size", "NUMERIC(15,2)"),
    ("showroom_visits", "architect_name", "VARCHAR(200)"),
    ("showroom_visits", "builder_name", "VARCHAR(200)"),
    ("showroom_visits", "lead_temperature", "VARCHAR(20)"),
    ("showroom_visits", "lead_source", "VARCHAR(50)"),
    ("showroom_visits", "referral_name", "VARCHAR(200)"),
    ("showroom_visits", "referral_contact", "VARCHAR(20)"),
    ("showroom_visits", "time_spent_minutes", "INTEGER"),
    ("showroom_visits", "presentation_shared", "BOOLEAN DEFAULT FALSE"),
    ("showroom_visits", "video_3d_shared", "BOOLEAN DEFAULT FALSE"),
    ("showroom_visits", "follow_up_date", "TIMESTAMP WITH TIME ZONE"),
]


def migrate():
    with engine.connect() as conn:
        for table, column, col_type in COLUMNS:
            conn.execute(text(
                f"ALTER TABLE {table} ADD COLUMN IF NOT EXISTS {column} {col_type}"
            ))
        conn.commit()
    print("✓ PDF field columns migrated")


if __name__ == "__main__":
    migrate()
