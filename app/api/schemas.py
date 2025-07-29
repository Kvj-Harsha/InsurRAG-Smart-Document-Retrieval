# Defines request and response models using pydantic.
# Ensures input validation and OpenAPI documentation.
from pydantic import BaseModel, Field
from typing import List, Optional, Union

class HackRxRunRequest(BaseModel):
    """
    Schema for the /hackrx/run API request.
    Accepts a document URL and a list of natural language questions.
    """
    documents: str = Field(..., description="URL to the document (.pdf or .docx) to be processed.")
    questions: List[str] = Field(..., description="A list of natural language questions to ask the document.")

class HackRxRunResponse(BaseModel):
    """
    Schema for the /hackrx/run API successful response (HTTP 200).
    """
    answers: List[str] = Field(default_factory=list, description="A list of generated answers corresponding to the questions.")
    latency_ms: int = Field(..., description="The total latency of the request in milliseconds.")
    # Note: source_chunks are not explicitly mentioned in the new spec's 200 response,
    # but could be added back if desired for debugging/transparency.
    # source_chunks: List[str] = Field(default_factory=list, description="A list of text chunks from the document that were used to generate the answer.")

class ErrorResponse(BaseModel):
    """
    Generic schema for API error responses (HTTP 400, 401, 500).
    """
    error: str = Field(..., description="Description of the error that occurred.")

class HealthCheckResponse(BaseModel):
    """
    Schema for the /health API response.
    """
    status: str = Field(..., description="Status of the API (e.g., 'healthy', 'unhealthy').")
    version: str = Field(..., description="Current API version.")
    uptime_seconds: int = Field(..., description="API uptime in seconds.")
    message: Optional[str] = Field(None, description="Optional health message.")

