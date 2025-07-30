from fastapi import FastAPI, HTTPException, Depends, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
from typing import List, Optional

from app.services.parser import document_parser
from app.services.chunker import chunk_text
from app.services.embedder import embedder
from app.services.vector_store import upsert_embeddings
from app.services.qa import answer_query

security = HTTPBearer()
API_KEY = "hackrx-secret-key"  # 🔐 Change this in production (env var)

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    if credentials.credentials != API_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

app = FastAPI(title="HackRx RAG API")

class HackRxRequest(BaseModel):
    documents: str
    questions: List[str]
    namespace: Optional[str] = "default"
    top_k: Optional[int] = 3

@app.post("/hackrx/run", dependencies=[Depends(verify_token)])
async def hackrx_run(payload: HackRxRequest):
    doc_url = payload.documents
    questions = payload.questions
    namespace = payload.namespace
    top_k = payload.top_k

    # Parse the document
    parsed_text, mime_type = await document_parser.parse_document(doc_url)
    if not parsed_text:
        raise HTTPException(status_code=400, detail="Failed to parse document.")

    # Chunk & embed
    chunks = chunk_text(parsed_text)
    embeddings = await embedder.embed_texts(chunks, task_type="search_document")
    if not embeddings:
        raise HTTPException(status_code=500, detail="Embedding failed.")
    await upsert_embeddings(embeddings, chunks, namespace=namespace)

    # Answer questions
    answers = []
    for question in questions:
        answer = await answer_query(question, top_k=top_k, namespace=namespace)
        answers.append(answer)

    return {"answers": answers}


# ✅ Custom OpenAPI with Bearer Auth in Swagger UI
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="HackRx RAG API",
        version="1.0.0",
        description="Submit document + questions to get smart answers.",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
