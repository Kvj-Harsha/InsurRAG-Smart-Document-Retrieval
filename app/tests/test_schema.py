# test_schemas.py
from app.api.schemas import HackRxRunRequest, HackRxRunResponse, ErrorResponse, HealthCheckResponse
import json

def run_schema_tests():
    print("--- Testing HackRxRunRequest Schema ---")
    try:
        req = HackRxRunRequest(
            documents="https://example.com/document.pdf",
            questions=["What is the main topic?", "Who is the author?"]
        )
        print(f"Valid HackRxRunRequest: {req.model_dump_json(indent=2)}")
    except Exception as e:
        print(f"Error creating HackRxRunRequest: {e}")

    print("\n--- Testing HackRxRunResponse Schema ---")
    try:
        res = HackRxRunResponse(
            answers=["The main topic is RAG.", "The author is John Doe."],
            latency_ms=250
        )
        print(f"Valid HackRxRunResponse: {res.model_dump_json(indent=2)}")
    except Exception as e:
        print(f"Error creating HackRxRunResponse: {e}")

    print("\n--- Testing ErrorResponse Schema ---")
    try:
        err = ErrorResponse(error="Unauthorized access: Invalid API key.")
        print(f"Valid ErrorResponse: {err.model_dump_json(indent=2)}")
    except Exception as e:
        print(f"Error creating ErrorResponse: {e}")

    print("\n--- Testing HealthCheckResponse Schema ---")
    try:
        health = HealthCheckResponse(status="healthy", version="2.0.0", uptime_seconds=3600)
        print(f"Valid HealthCheckResponse: {health.model_dump_json(indent=2)}")
    except Exception as e:
        print(f"Error creating HealthCheckResponse: {e}")

if __name__ == "__main__":
    run_schema_tests()