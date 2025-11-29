import sys
import os
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.api.server import app
from src.schemas.match_response import MatchResponse

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

@patch('src.api.controllers.matching_controller.matching_engine')
def test_match_vehicle_endpoint(mock_engine):
    # Mock response
    mock_engine.process.return_value = MatchResponse(
        match=True,
        vehicle_id="test_id",
        confidence=0.9,
        llm_used=False
    )
    
    payload = {"partner_id": "123", "vehicle_name": "Test Vehicle"}
    response = client.post("/match/", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["match"] is True
    assert data["vehicle_id"] == "test_id"

@patch('src.api.controllers.matching_controller.matching_engine')
def test_match_batch_endpoint(mock_engine):
    # Mock response
    mock_engine.process.return_value = MatchResponse(
        match=True,
        vehicle_id="test_id",
        confidence=0.9
    )
    
    payload = [
        {"partner_id": "1", "vehicle_name": "V1"},
        {"partner_id": "2", "vehicle_name": "V2"}
    ]
    response = client.post("/match/batch", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["match"] is True
