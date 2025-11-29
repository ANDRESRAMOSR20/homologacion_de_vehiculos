from sentence_transformers import SentenceTransformer
from src.core.config.settings import settings
import logging

logger = logging.getLogger(__name__)

class EmbeddingService:
    def __init__(self):
        logger.info(f"Loading embedding model: {settings.MODEL_NAME}")
        self.model = SentenceTransformer(settings.MODEL_NAME)

    def generate_embeddings(self, texts: list[str]):
        """
        Generates embeddings for a list of texts.
        """
        if not texts:
            return []
        
        logger.info(f"Generating embeddings for {len(texts)} texts")
        embeddings = self.model.encode(texts, show_progress_bar=True)
        return embeddings

embedding_service = EmbeddingService()
