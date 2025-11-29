import sys
import os
import pytest
from unittest.mock import MagicMock, patch

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.core.matching.matching_engine import MatchingEngine
from src.schemas.match_response import MatchResponse

@pytest.fixture
def mock_dependencies():
    with patch('src.core.matching.matching_engine.normalizer') as mock_norm, \
         patch('src.core.matching.matching_engine.embedding_service') as mock_embed, \
         patch('src.core.matching.matching_engine.similarity_service') as mock_sim, \
         patch('src.core.matching.matching_engine.llm_service') as mock_llm, \
         patch('src.core.matching.matching_engine.settings') as mock_settings:
        
        yield mock_norm, mock_embed, mock_sim, mock_llm, mock_settings

def test_matching_engine_success(mock_dependencies):
    mock_norm, mock_embed, mock_sim, mock_llm, mock_settings = mock_dependencies
    
    # Setup
    mock_norm.normalize.return_value = "normalized vehicle"
    mock_embed.generate_embeddings.return_value = [[0.1, 0.2, 0.3]]
    # Hybrid search returns list of (id, name, score)
    mock_sim.search.return_value = [("vehicle_123", "Vehicle Name", 0.95)]
    mock_settings.SIM_THRESHOLD = 0.8
    
    engine = MatchingEngine()
    response = engine.process("Input Vehicle")
    
    assert response.match is True
    assert response.vehicle_id == "vehicle_123"
    assert response.confidence == 0.95
    assert response.llm_used is False

def test_matching_engine_low_confidence(mock_dependencies):
    mock_norm, mock_embed, mock_sim, mock_llm, mock_settings = mock_dependencies
    
    # Setup
    mock_norm.normalize.return_value = "normalized vehicle"
    mock_embed.generate_embeddings.return_value = [[0.1, 0.2, 0.3]]
    # Very low score, below 0.4 threshold for LLM
    mock_sim.search.return_value = [("vehicle_123", "Vehicle Name", 0.3)]
    mock_settings.SIM_THRESHOLD = 0.8
    
    engine = MatchingEngine()
    response = engine.process("Input Vehicle")
    
    assert response.match is False
    assert response.vehicle_id is None
    
def test_matching_engine_llm_fallback_middle_score(mock_dependencies):
    mock_norm, mock_embed, mock_sim, mock_llm, mock_settings = mock_dependencies
    
    # Setup
    mock_norm.normalize.return_value = "normalized vehicle"
    mock_embed.generate_embeddings.return_value = [[0.1, 0.2, 0.3]]
    # Score between 0.4 and 0.8
    mock_sim.search.return_value = [("vehicle_123", "Vehicle Name", 0.65)] 
    mock_settings.SIM_THRESHOLD = 0.8
    
    mock_llm.resolve_conflict.return_value = ("vehicle_123", 0.65)
    
    engine = MatchingEngine()
    response = engine.process("Input Vehicle")
    
    assert response.match is True
    assert response.vehicle_id == "vehicle_123"
    assert response.llm_used is True

def test_matching_engine_llm_fallback_ambiguity(mock_dependencies):
    mock_norm, mock_embed, mock_sim, mock_llm, mock_settings = mock_dependencies
    
    # Setup
    mock_norm.normalize.return_value = "normalized vehicle"
    mock_embed.generate_embeddings.return_value = [[0.1, 0.2, 0.3]]
    # High score but ambiguous (close second)
    mock_sim.search.return_value = [("vehicle_A", "Vehicle A", 0.85), ("vehicle_B", "Vehicle B", 0.82)]
    mock_settings.SIM_THRESHOLD = 0.8
    
    mock_llm.resolve_conflict.return_value = ("vehicle_A", 0.85)
    
    engine = MatchingEngine()
    response = engine.process("Input Vehicle")
    
    assert response.llm_used is True
    assert response.vehicle_id == "vehicle_A"

def test_matching_engine_empty_input(mock_dependencies):
    mock_norm, _, _, _, _ = mock_dependencies
    mock_norm.normalize.return_value = ""
    
    engine = MatchingEngine()
    response = engine.process("")
    
    assert response.match is False
    assert "Empty" in response.details
