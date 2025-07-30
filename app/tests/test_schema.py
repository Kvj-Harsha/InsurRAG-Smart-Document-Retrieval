import asyncio
from app.services.embedder import embedder
from app.services.vector_store import upsert_embeddings

async def main():
    texts = ["Chunk A", "Chunk B"]
    embeddings = await embedder.embed_texts(texts)

    if embeddings:
        upsert_embeddings(texts, embeddings)
        print("✅ Embeddings upserted to Pinecone.")
    else:
        print("❌ Failed to generate embeddings.")

# Entry point
if __name__ == "__main__":
    asyncio.run(main())
