# app/services/embedding.py

from typing import List, Optional
from sentence_transformers import SentenceTransformer

class Embedder:
    def __init__(self): 
        self.model_name = "all-MiniLM-L6-v2"  # You can change this model
        self.model = SentenceTransformer(self.model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()

    async def embed_texts(self, texts: List[str], task_type: str = "search_document") -> Optional[List[List[float]]]:
        if not texts:
            return []

        try:
            embeddings = self.model.encode(texts, convert_to_numpy=True).tolist()
            return embeddings
        except Exception as e:
            print(f"Embedding error: {e}")
            return None

embedder = Embedder()
