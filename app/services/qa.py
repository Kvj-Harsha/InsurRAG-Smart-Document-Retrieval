from app.services.retriever import retriever
from app.utils.llm_client import groq  # Wrapper around Groq API

async def answer_query(query: str, top_k: int = 3, namespace: str = "default") -> str:
    print(f"🧪 Answering query: '{query}'")

    # Step 1: Retrieve top-k matching chunks
    docs = await retriever.retrieve(query, top_k=top_k, namespace=namespace)
    if not docs:
        return "❌ No relevant documents found."

    # Step 2: Build context from retrieved documents
    context_chunks = [
        doc["metadata"].get("text") or doc["metadata"].get("content", "") for doc in docs
    ]
    context = "\n\n".join(context_chunks).strip()

    print(f"📚 Retrieved context (truncated):\n{context[:500]}...\n")

    # Step 3: Compose deterministic, assertive prompt
    prompt = (
        f"Context:\n{context}\n\n"
        f"Question: {query}\nAnswer:"
    )

    # Step 4: Query Groq
    try:
        response = await groq.ask(prompt)
        return response.strip()
    except Exception as e:
        return f"❌ Error querying Groq: {e}"
