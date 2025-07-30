# app/rag_pipeline.py

import asyncio
from app.services.parser import document_parser
from app.services.chunker import chunk_text
from app.services.embedder import embedder
from app.services.vector_store import upsert_embeddings
from app.services.retriever import retriever
from app.services.qa import answer_query


async def run_rag_pipeline(doc_url: str, question: str, namespace: str = "default", top_k: int = 3):
    print(f"\n🔗 Parsing document from: {doc_url}")
    parsed_text, mime_type = await document_parser.parse_document(doc_url)

    if not parsed_text:
        print("❌ Failed to parse document.")
        return None

    print(f"📄 Document parsed successfully. Length: {len(parsed_text)} characters")

    # Chunk the document
    chunks = chunk_text(parsed_text)
    print(f"✂️ Chunked into {len(chunks)} parts.")

    # Embed the chunks
    embeddings = await embedder.embed_texts(chunks, task_type="search_document")
    if not embeddings or len(embeddings) != len(chunks):
        print("❌ Embedding failed or mismatch with chunk count.")
        return None

    print(f"🧠 Generated {len(embeddings)} embeddings. Upserting to Pinecone...")

    try:
        await upsert_embeddings(embeddings, chunks, namespace=namespace)
        print("✅ Embeddings upserted.")
    except Exception as e:
        print(f"❌ Error during upsert: {e}")
        return None

    # Retrieve relevant chunks
    print(f"\n🔍 Retrieving top {top_k} chunks for question: '{question}'")
    retrieved_docs = await retriever.retrieve(question, top_k=top_k, namespace=namespace)
    if not retrieved_docs:
        print("❌ Retrieval failed.")
        return None

    # Get the final answer
    print("🤖 Generating answer with Gemini...")
    try:
        answer = await answer_query(question, top_k=top_k, namespace=namespace)
    except Exception as e:
        print(f"❌ Error during answer generation: {e}")
        return None

    return answer


if __name__ == "__main__":
    import sys

    try:
        doc_url = input("🔗 Enter document URL (PDF/Web): ").strip()
        question = input("❓ Enter your question: ").strip()

        result = asyncio.run(run_rag_pipeline(doc_url, question))
        print("\n📘 Final Answer:")
        print(result or "No answer returned.")

    except KeyboardInterrupt:
        print("\n⛔ Interrupted by user.")
        sys.exit(0)
