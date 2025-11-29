from fastapi import APIRouter, HTTPException
from typing import List
from src.schemas.match_request import MatchRequest
from src.schemas.match_response import MatchResponse
from src.api.controllers.matching_controller import matching_controller

router = APIRouter(
    prefix="/match",
    tags=["matching"]
)

@router.post("/", response_model=MatchResponse)
async def match_vehicle(request: MatchRequest):
    try:
        return matching_controller.match_vehicle(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/batch", response_model=List[MatchResponse])
async def match_batch(requests: List[MatchRequest]):
    try:
        return matching_controller.match_batch(requests)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/metrics")
async def get_metrics():
    return matching_controller.get_metrics()
