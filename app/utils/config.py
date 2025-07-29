import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
# This is useful for local development to keep sensitive info out of code
load_dotenv()

class Config:
    """
    Configuration class for the RAG Chatbot API.
    Loads settings from environment variables with sensible defaults.
    """

    # --- API Settings ---
    PROJECT_NAME: str = "Fast RAG Chatbot API"
    API_VERSION: str = "2.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))

    # --- Groq LLM Settings ---
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL_NAME: str = os.getenv("GROQ_MODEL_NAME", "llama3-70b-8192")
    GROQ_TEMPERATURE: float = float(os.getenv("GROQ_TEMPERATURE", "0.1"))
    GROQ_MAX_TOKENS: int = int(os.getenv("GROQ_MAX_TOKENS", "2048"))

    # --- Nomic Embed Settings ---
    # Nomic Embed API endpoint
    NOMIC_EMBED_API_URL: str = os.getenv(
        "NOMIC_EMBED_API_URL", "https://api-inference.huggingface.co/models/nomic-ai/nomic-embed-text-v1.5"
    )
    # A Hugging Face API token might be required for Nomic Embed if used via Hugging Face Inference API
    # Alternatively, if self-hosting Nomic Embed, this might not be needed.
    NOMIC_EMBED_API_KEY: str = os.getenv("NOMIC_EMBED_API_KEY", "nk-GrvdvTgT7E-u7-886OZba0rJv2GffSzMpI5wZLgTNT0")
    NOMIC_EMBED_DIMENSION: int = int(os.getenv("NOMIC_EMBED_DIMENSION", "768")) # Default dimension for Nomic Embed v1.5

    # --- Weaviate Vector DB Settings ---
    WEAVIATE_URL: str = os.getenv("WEAVIATE_URL", "http://localhost:8080")
    WEAVIATE_API_KEY: str = os.getenv("WEAVIATE_API_KEY", "") # For Weaviate Cloud or authenticated instances
    WEAVIATE_COLLECTION_NAME: str = os.getenv("WEAVIATE_COLLECTION_NAME", "DocumentChunks")
    WEAVIATE_BATCH_SIZE: int = int(os.getenv("WEAVIATE_BATCH_SIZE", "100"))

    # --- Document Processing Settings ---
    MAX_DOCUMENT_SIZE_MB: int = int(os.getenv("MAX_DOCUMENT_SIZE_MB", "20"))
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "200"))
    # Supported file types for parsing
    SUPPORTED_FILE_TYPES: list[str] = [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document", # .docx
        "application/vnd.ms-outlook", # .msg
        "message/rfc822" # .eml
    ]

    # --- Security Settings ---
    API_KEY_AUTH_ENABLED: bool = os.getenv("API_KEY_AUTH_ENABLED", "False").lower() == "true"
    # In a real app, you'd hash and store API keys securely.
    # For simplicity, this is a placeholder.
    API_KEYS: list[str] = os.getenv("API_KEYS", "").split(",") if os.getenv("API_KEYS") else []

    # --- Logging Settings ---
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()
    LOG_FORMAT: str = os.getenv("LOG_FORMAT", "json") # or "console" for development

# Instantiate the config
settings = Config()

if __name__ == "__main__":
    # This block allows you to test if the config loads correctly
    # and to see the loaded values.
    print("--- Configuration Settings ---")
    print(f"Project Name: {settings.PROJECT_NAME}")
    print(f"Debug Mode: {settings.DEBUG}")
    print(f"Groq Model: {settings.GROQ_MODEL_NAME}")
    print(f"Weaviate URL: {settings.WEAVIATE_URL}")
    print(f"Max Document Size (MB): {settings.MAX_DOCUMENT_SIZE_MB}")
    print(f"Supported File Types: {settings.SUPPORTED_FILE_TYPES}")
    print(f"API Key Auth Enabled: {settings.API_KEY_AUTH_ENABLED}")
    print(f"Log Level: {settings.LOG_LEVEL}")

    # Example of setting an environment variable and seeing it reflected
    os.environ["GROQ_MODEL_NAME"] = "llama3-8b-8192"
    temp_settings = Config() # Re-instantiate to pick up new env var
    print(f"\n--- After setting GROQ_MODEL_NAME env var ---")
    print(f"Groq Model (after env var): {temp_settings.GROQ_MODEL_NAME}")
    del os.environ["GROQ_MODEL_NAME"] # Clean up
