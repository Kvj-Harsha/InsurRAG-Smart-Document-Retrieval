# app/tests/test_qa.py

import asyncio
from app.services.qa import answer_query

async def test_qa():
    query = "What is artificial intelligence?"
    answer = await answer_query(query, top_k=3)
    print("\n📘 Answer from Gemini:")
    print(answer)

if __name__ == "__main__":
    asyncio.run(test_qa())
