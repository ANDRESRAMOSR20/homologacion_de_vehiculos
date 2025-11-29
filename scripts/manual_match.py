import sys
import os
import argparse

# Add project root to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.core.db.database import SessionLocal
from src.core.db.models.partner_vehicle import PartnerVehicle

def manual_match(partner_id: int, match_id: str):
    db = SessionLocal()
    try:
        vehicle = db.query(PartnerVehicle).filter(PartnerVehicle.id == partner_id).first()
        
        if not vehicle:
            print(f"Partner vehicle with ID {partner_id} not found.")
            return

        print(f"Vehicle found: {vehicle.description}")
        print(f"Current Match ID: {vehicle.match_id}")
        
        vehicle.match_id = match_id
        vehicle.processed = True
        
        db.commit()
        print(f"Successfully updated vehicle {partner_id} with match_id: {match_id}")

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manually assign a match ID to a partner vehicle.")
    parser.add_argument("partner_id", type=int, help="The ID of the partner vehicle (from database)")
    parser.add_argument("match_id", type=str, help="The target Vehicle ID to assign")
    
    args = parser.parse_args()
    manual_match(args.partner_id, args.match_id)
