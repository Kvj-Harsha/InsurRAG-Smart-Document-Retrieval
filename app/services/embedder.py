from typing import List, Optional
from nomic import embed # Import the nomic embed function directly

from app.utils.config import settings
# from app.utils.logger import setup_logging # Removed logging import

class Embedder:
    """
    Handles generating embeddings for text chunks using the Nomic Embed model
    via the Nomic SDK.
    """
    def __init__(self):
        # The Nomic SDK typically picks up NOMIC_API_KEY from environment variables automatically.
        # We'll still log a warning if it's not set for clarity.
        # if not settings.NOMIC_EMBED_API_KEY: # Removed logging warning
        #     logger.warning("NOMIC_EMBED_API_KEY is not set. Nomic SDK calls might fail if authentication is required.")
        self.dimension = settings.NOMIC_EMBED_DIMENSION

    async def embed_texts(self, texts: List[str], task_type: str = "search_document") -> Optional[List[List[float]]]:
        """
        Generates embeddings for a list of texts using the Nomic SDK.

        Args:
            texts: A list of strings to embed.
            task_type: The task instruction prefix for Nomic Embed.
                       Common values: "search_document", "search_query", "clustering", "classification".
                       Defaults to "search_document" for document chunks.

        Returns:
            A list of lists of floats, where each inner list is an embedding vector.
            Returns None if the embedding fails.
        """
        if not texts:
            return []

        try:
            # logger.info(f"Sending {len(texts)} texts to Nomic SDK for embedding (task_type: {task_type}).") # Removed logging
            # Call Nomic SDK's embed.text function
            # The Nomic SDK handles the API request, authentication, and response parsing internally.
            embedding_response = embed.text(
                texts=texts,
                model='nomic-embed-text-v1.5', # Hardcoded as per your project plan
                task_type=task_type,
                dimensionality=self.dimension,
                # The NOMIC_API_KEY is usually picked up from the environment by the SDK.
                # If it needs to be explicitly passed, it would be 'api_key=settings.NOMIC_EMBED_API_KEY'
            )

            if embedding_response and 'embeddings' in embedding_response:
                # logger.info(f"Successfully generated embeddings for {len(texts)} texts.") # Removed logging
                return embedding_response['embeddings']
            else:
                # logger.error(f"Nomic SDK response missing 'embeddings' key or malformed: {embedding_response}") # Removed logging
                return None

        except Exception as e:
            # logger.error(f"An error occurred during embedding with Nomic SDK: {e}") # Removed logging
            return None

# Instantiate the embedder for use in other modules
embedder = Embedder()

if __name__ == "__main__":
    # This block is for testing the embedder functionality directly.
    import asyncio
    import os

    # Set up logging for direct script execution
    # setup_logging() # Removed logging setup
    # logger.setLevel(logging.DEBUG) # Removed logging level setting

    async def test_embedder():
        print("\n--- Testing Embedder with Nomic SDK ---")

        # Set a dummy API key for testing if not already set in .env
        # The Nomic SDK expects the API key in the NOMIC_API_KEY environment variable.
        # Ensure your .env file has NOMIC_API_KEY="your_nomic_api_key_here"
        if not settings.NOMIC_EMBED_API_KEY:
            print("WARNING: NOMIC_EMBED_API_KEY is not set in config. "
                  "Please ensure it's set in your .env file or environment variables "
                  "for Nomic SDK to authenticate. Using a placeholder for this test.")
            # For testing, you might temporarily set it here if not in .env
            # os.environ["NOMIC_API_KEY"] = "YOUR_NOMIC_API_KEY_HERE" # Replace with a valid Nomic API key

        test_texts_document = [
            "This is a sample document chunk about artificial intelligence.",
            "Machine learning is a subset of AI that enables systems to learn from data.",
            "The quick brown fox jumps over the lazy dog."
        ]
        test_texts_query = [
            "What is AI?",
            "Explain machine learning."
        ]
        empty_texts = []

        print("\n--- Embedding document texts ---")
        doc_embeddings = await embedder.embed_texts(test_texts_document, task_type="search_document")
        if doc_embeddings:
            print(f"Generated {len(doc_embeddings)} document embeddings. First embedding shape: {len(doc_embeddings[0])}")
            # print(f"First document embedding (first 5 dims): {doc_embeddings[0][:5]}...")
        else:
            print("Failed to generate document embeddings.")

        print("\n--- Embedding query texts ---")
        query_embeddings = await embedder.embed_texts(test_texts_query, task_type="search_query")
        if query_embeddings:
            print(f"Generated {len(query_embeddings)} query embeddings. First embedding shape: {len(query_embeddings[0])}")
            # print(f"First query embedding (first 5 dims): {query_embeddings[0][:5]}...")
        else:
            print("Failed to generate query embeddings.")

        print("\n--- Embedding empty list ---")
        empty_embeddings = await embedder.embed_texts(empty_texts)
        if empty_embeddings is not None:
            print(f"Generated {len(empty_embeddings)} embeddings for empty list (expected 0).")
        else:
            print("Failed to handle empty list for embedding.")

    # Run the async test function
    asyncio.run(test_embedder())
