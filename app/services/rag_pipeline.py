# app/services/rag_pipeline.py

from app.services.parser import parse_file
from app.services.chunker import chunk_text
from app.services.embedder import get_embeddings, search_similar_chunks
from app.services.llm import generate_answer

async def run_rag(doc_url: str, questions: list[str]) -> list[str]:
    # Step 1: Download and extract text
    raw_text = await parse_file(doc_url)

    # Step 2: Chunk it
    chunks = chunk_text(raw_text)

    # Step 3: Embed and store in Weaviate
    await get_embeddings(chunks)

    answers = []

    # Step 4: For each question:
    for question in questions:
        # a. Retrieve top-k relevant chunks
        top_chunks = await search_similar_chunks(question, k=5)
        context = "\n".join(top_chunks)

        # b. Generate answer using Groq
        answer = await generate_answer(context, question)
        answers.append(answer)

    return answers
