# app/tests/test_embedder.py

import asyncio
from app.services.embedder import embedder

async def test_embedder():
    print("🔍 Testing Nomic Embedder")

    sample_texts = [
        "Large language models are revolutionizing AI.",
        "Vector embeddings enable similarity search in RAG systems.",
        "Short string just to test."
    ]

    embeddings = await embedder.embed_texts(sample_texts, task_type="search_document")

    if embeddings:
        print(f"✅ Generated {len(embeddings)} embeddings.")
        print(f"📏 Each embedding vector has {len(embeddings[0])} dimensions.")
        print(f"🔢 First few values of first embedding: {embeddings[0][:5]}")
    else:
        print("❌ Failed to generate embeddings. Check your API key and internet connection.")

if __name__ == "__main__":
    asyncio.run(test_embedder())
