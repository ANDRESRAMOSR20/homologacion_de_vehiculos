"""seed vehicles

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
import csv
import os
import sys
from sqlalchemy import text

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../../')))

from src.core.db.database import SessionLocal
from src.core.db.models.vehicle import Vehicle

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    db = SessionLocal()
    try:
        # Path to the CSV file (relative to this script)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(current_dir, 'vehiculos_seguros.csv')
        
        if not os.path.exists(csv_path):
            print(f"CSV file not found at {csv_path}")
            return

        print(f"Seeding data from {csv_path}...")
        
        with open(csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            vehicles = []
            for row in reader:
                # Map CSV columns to model fields
                # CSV: versionc, id_crabi
                vehicle = Vehicle(
                    id=row['id_crabi'],
                    name=row['versionc']
                )
                vehicles.append(vehicle)
            
            # Bulk insert
            db.add_all(vehicles)
            db.commit()
            print(f"Successfully seeded {len(vehicles)} vehicles.")
            
    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

def downgrade():
    db = SessionLocal()
    try:
        print("Deleting all vehicles...")
        db.execute(text("DELETE FROM vehicles"))
        db.commit()
        print("Vehicles deleted.")
    except Exception as e:
        print(f"Error deleting data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    # Allow running directly for testing
    upgrade()
