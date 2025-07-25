from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional

# Security setup
security = HTTPBearer()

# FastAPI app with OpenAPI security definitions
app = FastAPI(
    title="HackRx Test API",
    description="Basic API for HackRx endpoint testing",
    version="1.0.0",
    swagger_ui_init_oauth={},  # Enables the authorize button
    openapi_tags=[{"name": "HackRx", "description": "Submit questions and get answers"}]
)

# Request body schema
class QueryRequest(BaseModel):
    documents: Optional[str]
    questions: List[str]

# Mock answer mapping
mock_answers = {
    "a": "Apple",
    "b": "Banana",
    "c": "Cherry"
}

# Endpoint
@app.post("/hackrx/run", tags=["HackRx"])
async def hackrx_run(
    payload: QueryRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    if token != "test123":
        return JSONResponse(status_code=401, content={"error": "Unauthorized"})

    answers = [mock_answers.get(q.strip().lower(), "Unknown") for q in payload.questions]

    return {"answers": answers}
