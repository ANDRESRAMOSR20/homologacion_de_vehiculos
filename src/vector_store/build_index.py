import faiss
import pickle
import os
import numpy as np
from src.core.config.settings import settings
from src.core.matching.embedding_service import embedding_service
from src.core.db.database import SessionLocal
from src.core.db.models.vehicle import Vehicle
from src.core.normalization.normalizer import normalizer

def build_index():
    db = SessionLocal()
    try:
        # 1. Fetch all vehicles
        vehicles = db.query(Vehicle).all()
        if not vehicles:
            print("No vehicles found in database.")
            return

        print(f"Found {len(vehicles)} vehicles.")

        # 2. Normalize names
        vehicle_ids = []
        texts = []
        for v in vehicles:
            normalized_name = normalizer.normalize(v.name)
            if normalized_name:
                vehicle_ids.append((v.id, normalized_name))
                texts.append(normalized_name)

        if not texts:
            print("No valid texts to index.")
            return

        # 3. Generate embeddings
        print("Generating embeddings...")
        embeddings = embedding_service.generate_embeddings(texts)
        
        # Convert to float32 for FAISS
        embeddings = np.array(embeddings).astype('float32')

        # 4. Build FAISS index
        # Using IndexFlatL2 for simplicity, or IndexFlatIP for cosine similarity (normalized vectors)
        # SentenceTransformers usually produce normalized vectors, so IP (Inner Product) == Cosine Similarity
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatIP(dimension)
        index.add(embeddings)
        
        print(f"Index built with {index.ntotal} vectors.")

        # 5. Save index and mapping
        os.makedirs(os.path.dirname(settings.VECTOR_INDEX_PATH), exist_ok=True)
        
        faiss.write_index(index, settings.VECTOR_INDEX_PATH)
        print(f"Index saved to {settings.VECTOR_INDEX_PATH}")

        # Save ID mapping
        mapping_path = settings.VECTOR_INDEX_PATH.replace('.faiss', '_map.pkl')
        with open(mapping_path, 'wb') as f:
            pickle.dump(vehicle_ids, f)
        print(f"Mapping saved to {mapping_path}")

    finally:
        db.close()
