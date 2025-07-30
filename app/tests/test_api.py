# Tests HTTP endpoints using TestClient (FastAPI's test wrapper).
import asyncio
from app.services.retriever import retriever

async def test_retrieve():
    results = await retriever.retrieve("What is machine learning?")
    for match in results:
        print(f"Score: {match['score']:.4f}")
        print(f"Metadata: {match.get('metadata')}")
        print()

asyncio.run(test_retrieve())
