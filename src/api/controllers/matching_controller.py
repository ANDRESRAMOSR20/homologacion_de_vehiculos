from typing import List
from src.schemas.match_request import MatchRequest
from src.schemas.match_response import MatchResponse
from src.core.matching.matching_engine import matching_engine
import logging

from src.core.monitoring.metrics import metrics_service
import time

logger = logging.getLogger(__name__)

class MatchingController:
    def match_vehicle(self, request: MatchRequest) -> MatchResponse:
        start_time = time.time()
        logger.info(f"Received match request for: {request.vehicle_name}")
        
        response = matching_engine.process(request.vehicle_name)
        
        latency_ms = (time.time() - start_time) * 1000
        metrics_service.record_request(
            latency_ms=latency_ms,
            match_found=response.match,
            llm_used=response.llm_used
        )
        
        return response

    def match_batch(self, requests: List[MatchRequest]) -> List[MatchResponse]:
        logger.info(f"Received batch match request for {len(requests)} items")
        results = []
        for req in requests:
            # We could record metrics individually here or aggregate
            # For simplicity, let's record individually by calling match_vehicle logic internally
            # But to avoid overhead, we'll just process and record
            start_time = time.time()
            response = matching_engine.process(req.vehicle_name)
            latency_ms = (time.time() - start_time) * 1000
            
            metrics_service.record_request(
                latency_ms=latency_ms,
                match_found=response.match,
                llm_used=response.llm_used
            )
            results.append(response)
            
        return results

    def get_metrics(self):
        return metrics_service.get_stats()

matching_controller = MatchingController()
