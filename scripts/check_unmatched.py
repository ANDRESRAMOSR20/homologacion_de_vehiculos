import sys
import os

# Add project root to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.core.db.database import SessionLocal
from src.core.db.models.partner_vehicle import PartnerVehicle

def check_unmatched():
    db = SessionLocal()
    try:
        unmatched = db.query(PartnerVehicle).filter(PartnerVehicle.match_id == None).all()
        print(f"Found {len(unmatched)} unmatched vehicles:")
        for v in unmatched:
            print(f"- ID: {v.id}")
            print(f"  Description: {v.description}")
            print("-" * 50)
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_unmatched()
