from src.core.normalization.normalizer import normalizer
from src.core.matching.embedding_service import embedding_service
from src.core.matching.similarity_service import similarity_service
from src.core.matching.llm_service import llm_service
from src.core.config.settings import settings
from src.schemas.match_response import MatchResponse
import logging

logger = logging.getLogger(__name__)

class MatchingEngine:
    def process(self, input_text: str) -> MatchResponse:
        """
        Process an input vehicle name and return the best match.
        """
        # 1. Normalize
        normalized_text = normalizer.normalize(input_text)
        if not normalized_text:
            return MatchResponse(match=False, details="Empty input after normalization")

        # 2. Generate Embedding
        embedding = embedding_service.generate_embeddings([normalized_text])
        if len(embedding) == 0:
             return MatchResponse(match=False, details="Failed to generate embedding")
        
        # 3. Search in FAISS (Hybrid)
        # Get top-k candidates
        candidates = similarity_service.search(embedding[0], input_text=normalized_text, k=5, hybrid=True)
        
        if not candidates:
            return MatchResponse(match=False, details="No candidates found")

        # 4. Check Threshold
        best_match_id, best_match_name, best_score = candidates[0]
        
        # 5. LLM Logic
        # Trigger LLM if:
        # a) Score is decent but below high confidence threshold (e.g. 0.4 - 0.85)
        # b) Top 2 candidates are very close (Ambiguity)
        
        should_trigger_llm = False
        
        # Condition A: Middle range score
        if 0.4 <= best_score < settings.SIM_THRESHOLD:
            should_trigger_llm = True
            
        # Condition B: Ambiguity (Top 2 are close)
        if len(candidates) >= 2:
            second_score = candidates[1][2]
            if (best_score - second_score) < 0.05: # 5% difference
                should_trigger_llm = True

        if best_score >= settings.SIM_THRESHOLD and not should_trigger_llm:
            return MatchResponse(
                match=True,
                vehicle_id=best_match_id,
                confidence=best_score,
                llm_used=False
            )
            
        if should_trigger_llm:
             llm_result = llm_service.resolve_conflict(candidates, normalized_text)
             if llm_result:
                 lid, lscore = llm_result
                 return MatchResponse(
                     match=True,
                     vehicle_id=lid,
                     confidence=lscore,
                     llm_used=True,
                     details="Resolved by LLM"
                 )

        return MatchResponse(
            match=False, 
            confidence=best_score, 
            details=f"Best match below threshold {settings.SIM_THRESHOLD}"
        )

matching_engine = MatchingEngine()
