# app/services/qa.py

from app.services.retriever import retriever
from app.utils.llm_client import groq  # Wrapper around groq 2.5 API


async def answer_query(query: str, top_k: int = 3, namespace: str = "default") -> str:
    print(f"🧪 Answering query: '{query}'")

    # Step 1: Retrieve top-k matching chunks
    docs = await retriever.retrieve(query, top_k=top_k, namespace=namespace)
    if not docs:
        return "❌ No relevant documents found."

    # Step 2: Build context from retrieved documents
    context = "\n\n".join(
        doc["metadata"].get("text") or doc["metadata"].get("content") or "..." for doc in docs
    )

    print(f"📚 Retrieved context (truncated):\n{context[:500]}...\n")

    # Step 3: Compose prompt
    prompt = f"""
Answer the following question based on the context below:

Context:
{context}

Question: {query}
Answer:
"""

    # Step 4: Call groq
    try:
        response = await groq.ask(prompt)
        return response.strip()
    except Exception as e:
        return f"❌ Error querying groq: {e}"
