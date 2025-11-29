import csv
import os
import sys

# Add project root to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../../")))

from src.core.db.database import SessionLocal
from src.core.db.models.partner_vehicle import PartnerVehicle

def seed_partner_vehicles():
    db = SessionLocal()
    try:
        csv_path = os.path.join(os.path.dirname(__file__), "vehiculos_socios.csv")
        
        if not os.path.exists(csv_path):
            print(f"CSV file not found at {csv_path}")
            return

        print(f"Seeding partner vehicles from {csv_path}...")
        
        with open(csv_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            for row in reader:
                description = row.get("descripcion")
                if description:
                    # Check if exists to avoid duplicates (optional, but good practice)
                    exists = db.query(PartnerVehicle).filter(PartnerVehicle.description == description).first()
                    if not exists:
                        vehicle = PartnerVehicle(description=description)
                        db.add(vehicle)
                        count += 1
            
            db.commit()
            print(f"Successfully seeded {count} partner vehicles.")
            
    except Exception as e:
        print(f"Error seeding partner vehicles: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_partner_vehicles()
