"""
Update demo user display names in an existing database.
Safe to run multiple times.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from app.database import engine

UPDATES = [
    ("9876543210", "Rohit Sain", "Field Operations"),
    ("9876543211", "Namita Kaushal", "Marketing"),
    ("9876543212", "Rakesh Pandey", "Showroom Sales"),
    ("9876543214", "Pritpal Singh", "Executive"),
]


def update():
    with engine.connect() as conn:
        for mobile, name, department in UPDATES:
            conn.execute(
                text(
                    "UPDATE users SET full_name = :name, department = :department "
                    "WHERE mobile_number = :mobile"
                ),
                {"name": name, "department": department, "mobile": mobile},
            )
        conn.commit()
    print("✓ Demo user names updated:")
    for mobile, name, _ in UPDATES:
        print(f"  {mobile} → {name}")


if __name__ == "__main__":
    update()
