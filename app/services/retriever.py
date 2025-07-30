from app.services.embedder import embedder
from app.services.pinecone_client import index

class Retriever:
    async def retrieve(self, query: str, top_k: int = 3, namespace: str = "default"):
        print(f"\n🧠 Embedding query: '{query}'")

        # Ensure input is wrapped in a list
        query_embeddings = await embedder.embed_texts([query])
        
        if not query_embeddings or query_embeddings[0] is None:
            print("❌ Failed to generate query embedding.")
            return []

        query_embedding = query_embeddings[0]
        print(f"✅ Query embedding generated (dim={len(query_embedding)})")

        print(f"📨 Querying Pinecone index with top_k={top_k}...")
        try:
            response = index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True,
                namespace=namespace
            )
            return response.get('matches', [])
        except Exception as e:
            print(f"❌ Exception during Pinecone query: {e}")
            return []

retriever = Retriever()
