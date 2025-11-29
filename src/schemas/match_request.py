from pydantic import BaseModel

class MatchRequest(BaseModel):
    partner_id: str
    vehicle_name: str
