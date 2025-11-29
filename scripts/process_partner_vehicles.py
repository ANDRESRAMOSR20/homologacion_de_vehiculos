import sys
import os

# Add project root to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.core.db.database import SessionLocal
from src.core.db.models.partner_vehicle import PartnerVehicle
from src.core.db.models.vehicle import Vehicle
from src.core.matching.matching_engine import matching_engine

def process_vehicles():
    db = SessionLocal()
    try:
        # Fetch unprocessed vehicles
        vehicles = db.query(PartnerVehicle).filter(PartnerVehicle.processed == False).all()
        print(f"Found {len(vehicles)} unprocessed vehicles.")

        for v in vehicles:
            print(f"Processing ID {v.id}: {v.description}")
            try:
                result = matching_engine.process(v.description)
                
                if result.match:
                    v.match_id = result.vehicle_id
                    print(f"  -> Matched: {result.vehicle_id} (Confidence: {result.confidence:.2f})")
                else:
                    # No match found in official catalog.
                    # Create a new entry in the Unified Catalog (vehicles table)
                    new_id = f"SOC-{v.id:03d}" # e.g. SOC-001
                    print(f"  -> No match found. Registering as new vehicle: {new_id}")
                    
                    new_vehicle = Vehicle(id=new_id, name=v.description)
                    db.add(new_vehicle)
                    # We need to flush to ensure it doesn't conflict if we process same ID (unlikely here)
                    db.flush() 
                    
                    v.match_id = new_id
                
                v.processed = True
            except Exception as e:
                print(f"  -> Error processing vehicle: {e}")
        
        db.commit()
        print("Batch processing complete. Unified Catalog updated.")

    except Exception as e:
        print(f"Critical Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    process_vehicles()
