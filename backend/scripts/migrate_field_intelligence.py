"""
Field Intelligence module — PDF-aligned columns.
Safe to run multiple times.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from app.database import engine

COLUMNS = [
    ("sites", "current_vendor", "VARCHAR(200)"),
    ("sites", "material_used", "VARCHAR(500)"),
    ("sites", "purchase_rate", "NUMERIC(15,2)"),
    ("site_media", "latitude", "VARCHAR(50)"),
    ("site_media", "longitude", "VARCHAR(50)"),
    ("site_media", "captured_at", "TIMESTAMP WITH TIME ZONE"),
]

STAGE_MAP = """
UPDATE sites SET site_stage = CASE site_stage
  WHEN 'planning' THEN '10'
  WHEN 'foundation' THEN '30'
  WHEN 'structure' THEN '50'
  WHEN 'finishing' THEN '70'
  WHEN 'completed' THEN '100'
  ELSE site_stage
END
WHERE site_stage IN ('planning', 'foundation', 'structure', 'finishing', 'completed')
"""


def migrate():
    with engine.connect() as conn:
        for table, column, col_type in COLUMNS:
            conn.execute(text(
                f"ALTER TABLE {table} ADD COLUMN IF NOT EXISTS {column} {col_type}"
            ))
        conn.execute(text(STAGE_MAP))
        conn.commit()
    print("✓ Field intelligence columns migrated + site stages normalized")


if __name__ == "__main__":
    migrate()
