import sys
import os
from unittest.mock import MagicMock

# Add project root to sys.path
sys.path.append(os.getcwd())

from src.tests.test_matching import (
    test_matching_engine_success, 
    test_matching_engine_low_confidence, 
    test_matching_engine_llm_fallback_middle_score, 
    test_matching_engine_llm_fallback_ambiguity, 
    test_matching_engine_empty_input
)

def run_tests():
    print("Starting manual tests...")
    
    # Create mocks
    mock_norm = MagicMock()
    mock_embed = MagicMock()
    mock_sim = MagicMock()
    mock_llm = MagicMock()
    mock_settings = MagicMock()
    
    mock_dependencies = (mock_norm, mock_embed, mock_sim, mock_llm, mock_settings)
    
    try:
        print("Running test_matching_engine_success...")
        # Reset mocks
        mock_norm.reset_mock()
        mock_sim.reset_mock()
        
        # Setup
        mock_norm.normalize.return_value = "normalized vehicle"
        mock_embed.generate_embeddings.return_value = [[0.1, 0.2, 0.3]]
        mock_sim.search.return_value = [("vehicle_123", "Vehicle Name", 0.95)]
        mock_settings.SIM_THRESHOLD = 0.8
        
        test_matching_engine_success(mock_dependencies)
        print("PASS")
    except Exception as e:
        print(f"FAIL: {e}")
        import traceback
        traceback.print_exc()

    try:
        print("Running test_matching_engine_llm_fallback_ambiguity...")
        mock_norm.reset_mock()
        mock_sim.reset_mock()
        mock_llm.reset_mock()
        
        mock_norm.normalize.return_value = "normalized vehicle"
        mock_embed.generate_embeddings.return_value = [[0.1, 0.2, 0.3]]
        mock_sim.search.return_value = [("vehicle_A", "Vehicle A", 0.85), ("vehicle_B", "Vehicle B", 0.82)]
        mock_settings.SIM_THRESHOLD = 0.8
        mock_llm.resolve_conflict.return_value = ("vehicle_A", 0.85)
        
        test_matching_engine_llm_fallback_ambiguity(mock_dependencies)
        print("PASS")
    except Exception as e:
        print(f"FAIL: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_tests()
