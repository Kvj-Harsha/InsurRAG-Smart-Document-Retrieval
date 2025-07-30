# app/services/embedding.py

# TEMP: Hardcoded Nomic API Key for dev/testing
import os
os.environ["NOMIC_API_KEY"] = "nk-GrvdvTgT7E-u7-886OZba0rJv2GffSzMpI5wZLgTNT0" 

from typing import List, Optional
from nomic import embed
 # 🔁 Replace with your actual API key

class Embedder:
    def __init__(self):
        self.dimension = 768  # Or 1024 — set to your preferred model dimensionality

    async def embed_texts(self, texts: List[str], task_type: str = "search_document") -> Optional[List[List[float]]]:
        if not texts:
            return []

        try:
            response = embed.text(
                texts=texts,
                model='nomic-embed-text-v1.5',
                task_type='search_document',
                dimensionality=768# 👈 explicitly pass API key here
            )

            return response.get('embeddings') if response and 'embeddings' in response else None

        except Exception:
            return None

embedder = Embedder()
