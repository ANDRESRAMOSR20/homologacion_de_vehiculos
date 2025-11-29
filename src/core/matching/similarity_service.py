import faiss
import pickle
import os
import numpy as np
from src.core.config.settings import settings
import logging

logger = logging.getLogger(__name__)

class SimilarityService:
    def __init__(self):
        self.index = None
        self.vehicle_ids = []
        self._load_index()

    def _load_index(self):
        if not os.path.exists(settings.VECTOR_INDEX_PATH):
            logger.warning(f"Vector index not found at {settings.VECTOR_INDEX_PATH}")
            return

        try:
            logger.info(f"Loading vector index from {settings.VECTOR_INDEX_PATH}")
            self.index = faiss.read_index(settings.VECTOR_INDEX_PATH)
            
            mapping_path = settings.VECTOR_INDEX_PATH.replace('.faiss', '_map.pkl')
            if os.path.exists(mapping_path):
                with open(mapping_path, 'rb') as f:
                    self.vehicle_ids = pickle.load(f)
            else:
                logger.warning(f"Mapping file not found at {mapping_path}")
                
        except Exception as e:
            logger.error(f"Error loading index: {e}")

    def calculate_token_overlap(self, query: str, target: str) -> float:
        set_query = set(query.lower().split())
        set_target = set(target.lower().split())
        
        if not set_query:
            return 0.0
            
        intersection = len(set_query.intersection(set_target))
        # Score is percentage of query tokens found in target
        return intersection / len(set_query)

    def search(self, embedding: np.ndarray, input_text: str = "", k: int = 5, hybrid: bool = True) -> list:
        """
        Search for top-k similar vectors.
        If hybrid is True, re-ranks using Jaccard similarity.
        Returns list of (vehicle_id, score).
        """
        if self.index is None:
            logger.warning("Index not loaded, cannot search.")
            return []

        # Ensure embedding is float32 and 2D
        embedding = np.array(embedding).astype('float32')
        if len(embedding.shape) == 1:
            embedding = embedding.reshape(1, -1)

        # Retrieve more candidates for re-ranking
        search_k = k * 4 if hybrid else k
        scores, indices = self.index.search(embedding, search_k)
        
        candidates = []
        for score, idx in zip(scores[0], indices[0]):
            if idx != -1 and idx < len(self.vehicle_ids):
                # vehicle_ids contains (id, normalized_name) tuples
                vid_data = self.vehicle_ids[idx]
                if isinstance(vid_data, tuple):
                    vid, vname = vid_data
                else:
                    # Fallback for old index format
                    vid = vid_data
                    vname = str(vid)
                    
                candidates.append((vid, vname, float(score)))
        
        if not hybrid or not input_text:
            # Return (id, name, score)
            return candidates[:k]

        # Hybrid Re-ranking
        reranked = []
        for vid, vname, vec_score in candidates:
            # Calculate Token Overlap score using vname
            # This is better for "Short Query" vs "Long Description"
            overlap_score = self.calculate_token_overlap(input_text, vname)
            
            # Weighted combination: 60% Vector, 40% Overlap
            final_score = (0.6 * vec_score) + (0.4 * overlap_score)
            reranked.append((vid, vname, final_score))
            
        # Sort by final score descending
        reranked.sort(key=lambda x: x[2], reverse=True)
        
        return reranked[:k]

similarity_service = SimilarityService()
