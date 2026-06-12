"""
Marketing meeting module — PDF-aligned columns.
Safe to run multiple times.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from app.database import engine

COLUMNS = [
    ("meetings", "met_with", "VARCHAR(50)"),
    ("meetings", "firm_name", "VARCHAR(200)"),
    ("meetings", "address", "VARCHAR(500)"),
    ("meetings", "area", "VARCHAR(100)"),
    ("meetings", "city", "VARCHAR(100)"),
    ("meetings", "category", "VARCHAR(10)"),
    ("meetings", "relationship_stage", "VARCHAR(50)"),
]

RELATIONSHIP_MAP = """
UPDATE meetings SET relationship_stage = CASE relationship_score
  WHEN 'excellent' THEN 'trusted'
  WHEN 'good' THEN 'active_engagement'
  WHEN 'average' THEN 'rapport_building'
  WHEN 'poor' THEN 'introductory'
  WHEN 'new' THEN 'new'
  ELSE COALESCE(relationship_stage, 'introductory')
END
WHERE relationship_stage IS NULL AND relationship_score IS NOT NULL
"""


def migrate():
    with engine.connect() as conn:
        for table, column, col_type in COLUMNS:
            conn.execute(text(
                f"ALTER TABLE {table} ADD COLUMN IF NOT EXISTS {column} {col_type}"
            ))
        conn.execute(text(RELATIONSHIP_MAP))
        conn.commit()
    print("✓ Meeting PDF columns migrated")


if __name__ == "__main__":
    migrate()
