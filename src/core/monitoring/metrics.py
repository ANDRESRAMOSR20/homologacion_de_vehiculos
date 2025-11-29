import time
import logging
from dataclasses import dataclass, field
from typing import Dict

logger = logging.getLogger(__name__)

@dataclass
class Metrics:
    total_requests: int = 0
    successful_matches: int = 0
    failed_matches: int = 0
    llm_triggers: int = 0
    llm_successful_resolutions: int = 0
    total_latency_ms: float = 0.0
    
    @property
    def average_latency_ms(self) -> float:
        return self.total_latency_ms / self.total_requests if self.total_requests > 0 else 0.0
    
    @property
    def match_rate(self) -> float:
        return (self.successful_matches / self.total_requests * 100) if self.total_requests > 0 else 0.0

class MetricsService:
    def __init__(self):
        self._metrics = Metrics()
        
    def record_request(self, latency_ms: float, match_found: bool, llm_used: bool):
        self._metrics.total_requests += 1
        self._metrics.total_latency_ms += latency_ms
        
        if match_found:
            self._metrics.successful_matches += 1
        else:
            self._metrics.failed_matches += 1
            
        if llm_used:
            self._metrics.llm_triggers += 1
            if match_found:
                self._metrics.llm_successful_resolutions += 1
                
    def get_stats(self) -> Dict:
        return {
            "total_requests": self._metrics.total_requests,
            "successful_matches": self._metrics.successful_matches,
            "failed_matches": self._metrics.failed_matches,
            "match_rate_percent": round(self._metrics.match_rate, 2),
            "average_latency_ms": round(self._metrics.average_latency_ms, 2),
            "llm_stats": {
                "triggers": self._metrics.llm_triggers,
                "resolutions": self._metrics.llm_successful_resolutions,
                "resolution_rate_percent": round((self._metrics.llm_successful_resolutions / self._metrics.llm_triggers * 100) if self._metrics.llm_triggers > 0 else 0.0, 2)
            }
        }

metrics_service = MetricsService()
