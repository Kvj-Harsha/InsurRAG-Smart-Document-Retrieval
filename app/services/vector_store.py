import uuid
from typing import List
from app.services.pinecone_client import index


async def upsert_embeddings(embeddings: List[List[float]], texts: List[str], namespace: str = "default"):
    vectors = []
    for i, embedding in enumerate(embeddings):
        vector_id = str(uuid.uuid4())
        metadata = {"text": texts[i]}
        vectors.append({
            "id": vector_id,
            "values": embedding,
            "metadata": metadata
        })

    print(f"📥 Upserting {len(vectors)} vectors into Pinecone...")
    try:
        index.upsert(vectors=vectors, namespace=namespace)
    except Exception as e:
        print(f"❌ Exception during upsert_embeddings: {e}")
