import sys
import os

# Add project root to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.core.db.database import SessionLocal
from src.core.db.models.partner_vehicle import PartnerVehicle

def reset_processing():
    db = SessionLocal()
    try:
        # Reset vehicles that have no match_id (or all if needed, but let's target the unmatched ones first)
        # Actually, the user wants to re-process the ones that failed (match_id is None)
        # But wait, the previous script set processed=True even if match_id=None.
        
        vehicles = db.query(PartnerVehicle).filter(PartnerVehicle.match_id == None).all()
        print(f"Found {len(vehicles)} vehicles with no match.")
        
        for v in vehicles:
            v.processed = False
            print(f"Resetting ID {v.id}")
            
        db.commit()
        print("Reset complete.")

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    reset_processing()
