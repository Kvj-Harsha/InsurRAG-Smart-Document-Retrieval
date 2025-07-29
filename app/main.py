from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="HackRx API",
    description="Submit questions to the RAG chatbot",
    version="1.0.0"
)

app.include_router(router)


app.include_router(router)

if __name__ == "__main__":
    print("Main is running")

