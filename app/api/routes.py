# app/routes.py

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, HttpUrl
import requests
import tempfile

from app.services.parser import parse_file
from app.services.embedder import get_embeddings  # ✅ Uses OpenAI now

router = APIRouter()
security = HTTPBearer()
API_KEY = "test123"

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return credentials.credentials

class RunRequest(BaseModel):
    documents: HttpUrl

@router.post("/hackrx/run")
def run_pipeline(request: RunRequest, token: str = Depends(verify_token)):
    try:
        # 📥 Step 1: Download the PDF
        response = requests.get(str(request.documents))
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Could not fetch document")

        # 🧾 Step 2: Save locally
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(response.content)
            file_path = tmp.name

        # 📄 Step 3: Parse PDF
        chunks = parse_file(file_path)
        if not chunks:
            raise HTTPException(status_code=400, detail="No content extracted")

        # 🧠 Step 4: Get embeddings
        embeddings = get_embeddings(chunks)
        if not embeddings:
            raise HTTPException(status_code=500, detail="Embedding failed")

        return {
            "step": "parsed_and_embedded",
            "num_chunks": len(chunks),
            "chunks": chunks[:3],
            "embedding_sample": embeddings[0][:5]  # Preview first 5 dims
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG pipeline failed: {e}")
