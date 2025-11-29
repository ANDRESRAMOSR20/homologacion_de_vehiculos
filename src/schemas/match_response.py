from pydantic import BaseModel
from typing import Optional

class MatchResponse(BaseModel):
    match: bool
    vehicle_id: Optional[str] = None
    confidence: float = 0.0
    llm_used: bool = False
    details: Optional[str] = None
