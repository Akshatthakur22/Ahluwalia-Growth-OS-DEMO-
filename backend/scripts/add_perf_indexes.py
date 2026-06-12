"""
Add performance indexes for frequently filtered columns.
Safe to run multiple times (IF NOT EXISTS).
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from app.database import engine

INDEXES = [
    "CREATE INDEX IF NOT EXISTS ix_attendance_check_in_time ON attendance_logs (check_in_time)",
    "CREATE INDEX IF NOT EXISTS ix_attendance_user_check_in ON attendance_logs (user_id, check_in_time DESC)",
    "CREATE INDEX IF NOT EXISTS ix_opportunities_status ON opportunities (current_status)",
    "CREATE INDEX IF NOT EXISTS ix_opportunities_follow_up ON opportunities (follow_up_date)",
    "CREATE INDEX IF NOT EXISTS ix_opportunities_site_id ON opportunities (site_id)",
    "CREATE INDEX IF NOT EXISTS ix_meetings_conducted_by ON meetings (conducted_by)",
    "CREATE INDEX IF NOT EXISTS ix_meetings_meeting_date ON meetings (meeting_date DESC)",
    "CREATE INDEX IF NOT EXISTS ix_meetings_follow_up ON meetings (follow_up_date)",
    "CREATE INDEX IF NOT EXISTS ix_showroom_sales_exec ON showroom_visits (sales_executive_id)",
    "CREATE INDEX IF NOT EXISTS ix_showroom_visit_date ON showroom_visits (visit_date DESC)",
    "CREATE INDEX IF NOT EXISTS ix_sites_discovered_by ON sites (discovered_by)",
    "CREATE INDEX IF NOT EXISTS ix_sites_created_at ON sites (created_at DESC)",
    "CREATE INDEX IF NOT EXISTS ix_contacts_mobile ON contacts (mobile_number)",
    "CREATE INDEX IF NOT EXISTS ix_contacts_site_id ON contacts (site_id)",
    "CREATE INDEX IF NOT EXISTS ix_assignments_assigned_to ON assignments (assigned_to)",
    "CREATE INDEX IF NOT EXISTS ix_ownership_marketing ON ownership_records (marketing_owner_id)",
    "CREATE INDEX IF NOT EXISTS ix_ownership_sales ON ownership_records (sales_owner_id)",
]


def migrate():
    with engine.connect() as conn:
        for stmt in INDEXES:
            conn.execute(text(stmt))
        conn.commit()
    print(f"✓ {len(INDEXES)} performance indexes applied")


if __name__ == "__main__":
    migrate()
