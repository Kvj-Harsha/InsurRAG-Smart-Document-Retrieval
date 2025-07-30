import asyncio
from app.services.chunker import chunk_from_url

async def main():
    url = "https://arxiv.org/pdf/1706.03762.pdf"

    try:
        chunks = await chunk_from_url(url)
        print(f"✅ {len(chunks)} chunks generated.")
        for i, chunk in enumerate(chunks[:3]):
            print(f"\n--- Chunk {i+1} ---\n{chunk[:300]}...\n")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
