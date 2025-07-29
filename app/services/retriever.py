from typing import List, Dict, Any, Optional
from pinecone import Pinecone, Index, PodSpec # Import Pinecone classes
import asyncio # Needed for async operations in the test block
import time # Needed for time.sleep in the test block

from app.services.embedder import embedder # Import the embedder to create query embeddings

# --- Hardcoded Configuration (FOR TESTING/SIMPLICITY ONLY - NOT FOR PRODUCTION) ---
# IMPORTANT: Replace these with your actual Pinecone credentials
PINECONE_API_KEY = "pcsk_4Hnbb5_TvhMyxgRBqhUkCtGwB8gng2Piqu77nPWia1NgxJJnvJSn39VnUYf3iJih1C9gvT" # Your Pinecone API Key
PINECONE_ENVIRONMENT = "" # Your Pinecone environment (e.g., "gcp-starter", "us-west-2")
PINECONE_INDEX_NAME = "document-chunks" # Name of your Pinecone index

NOMIC_EMBED_DIMENSION = 768 # Dimension of embeddings from Nomic Embed v1.5

# --- END Hardcoded Configuration ---

class Retriever:
    """
    Handles interactions with the Pinecone vector database for storing and retrieving document chunks.
    """
    def __init__(self):
        self.pinecone_client: Optional[Pinecone] = None
        self.index: Optional[Index] = None
        self.index_name = PINECONE_INDEX_NAME
        self.embedding_dimension = NOMIC_EMBED_DIMENSION

        self._initialize_pinecone_client()

    def _initialize_pinecone_client(self):
        """
        Initializes the Pinecone client and connects to the specified index.
        """
        try:
            # Initialize Pinecone
            self.pinecone_client = Pinecone(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)

            # Check if index exists, create if not
            if self.index_name not in self.pinecone_client.list_indexes():
                print(f"Creating Pinecone index: {self.index_name} with dimension {self.embedding_dimension}")
                self.pinecone_client.create_index(
                    name=self.index_name,
                    dimension=self.embedding_dimension,
                    metric='cosine', # Cosine similarity is common for embeddings
                    spec=PodSpec(environment=PINECONE_ENVIRONMENT) # Required for serverless or starter tiers
                )
                print(f"Index '{self.index_name}' created successfully.")
            else:
                print(f"Index '{self.index_name}' already exists.")

            # Connect to the index
            self.index = self.pinecone_client.Index(self.index_name)
            print("Pinecone client initialized and connected to index successfully.")

        except Exception as e:
            print(f"Failed to initialize or connect to Pinecone: {e}")
            self.pinecone_client = None
            self.index = None

    async def add_document_chunks(self, chunks: List[str], source_url: str) -> bool:
        """
        Adds a list of text chunks to the Pinecone index.
        Embeddings are generated using the Nomic Embedder.
        """
        if not self.index:
            print("Pinecone index not ready. Cannot add document chunks.")
            return False

        print(f"Adding {len(chunks)} chunks to Pinecone index '{self.index_name}'.")
        try:
            vectors_to_upsert = []
            for i, chunk in enumerate(chunks):
                # Generate embedding for each chunk
                chunk_embedding = await embedder.embed_texts(texts=[chunk], task_type="search_document")
                if not chunk_embedding or not chunk_embedding[0]:
                    print(f"Failed to generate embedding for chunk {i}. Skipping.")
                    continue

                # Pinecone expects (id, vector, metadata)
                # We'll use a simple ID for now, e.g., "doc_chunk_{i}"
                vector_id = f"{source_url.replace('.', '_').replace('/', '_')}_chunk_{i}" # Simple ID from URL and index
                vectors_to_upsert.append({
                    "id": vector_id,
                    "values": chunk_embedding[0],
                    "metadata": {
                        "content": chunk,
                        "source_url": source_url,
                        "chunk_index": i
                    }
                })

            if vectors_to_upsert:
                # Upsert vectors to Pinecone
                self.index.upsert(vectors=vectors_to_upsert)
                print(f"Successfully added {len(vectors_to_upsert)} chunks to Pinecone.")
                return True
            else:
                print("No vectors to upsert.")
                return False
        except Exception as e:
            print(f"Error adding document chunks to Pinecone: {e}")
            return False

    async def retrieve_relevant_chunks(self, query: str, top_k: int = 5) -> List[str]:
        """
        Retrieves the most relevant document chunks from Pinecone based on a query.
        """
        if not self.index:
            print("Pinecone index not ready. Cannot retrieve chunks.")
            return []

        # Generate embedding for the query using our embedder service
        query_embedding = await embedder.embed_texts(texts=[query], task_type="search_query")
        if not query_embedding or not query_embedding[0]:
            print("Failed to generate embedding for the query. Cannot retrieve chunks.")
            return []

        try:
            print(f"Retrieving top {top_k} relevant chunks for query: '{query}'")
            # Perform a vector search in Pinecone
            query_results = self.index.query(
                vector=query_embedding[0],
                top_k=top_k,
                include_metadata=True # Ensure metadata is returned
            )

            retrieved_chunks = []
            for match in query_results.matches:
                if match.metadata and "content" in match.metadata:
                    retrieved_chunks.append(match.metadata["content"])

            print(f"Successfully retrieved {len(retrieved_chunks)} relevant chunks.")
            return retrieved_chunks
        except Exception as e:
            print(f"Error retrieving chunks from Pinecone: {e}")
            return []

# Instantiate the retriever for use in other modules
retriever = Retriever()

if __name__ == "__main__":
    async def test_retriever_simple():
        print("\n--- Simple Pinecone Retriever Test ---")

        # IMPORTANT: Replace these with your actual Pinecone credentials
        global PINECONE_API_KEY, PINECONE_ENVIRONMENT, NOMIC_EMBED_API_KEY
        PINECONE_API_KEY = "YOUR_PINECONE_API_KEY" # <--- REPLACE THIS
        PINECONE_ENVIRONMENT = "YOUR_PINECONE_ENVIRONMENT" # <--- REPLACE THIS (e.g., "gcp-starter")
        NOMIC_EMBED_API_KEY = "YOUR_NOMIC_API_KEY" # <--- REPLACE THIS

        # Re-initialize retriever with hardcoded keys for this test
        test_retriever_instance = Retriever()

        if not test_retriever_instance.index:
            print("Pinecone client or index not ready. Aborting retriever tests. Check your API keys and environment.")
            return

        # Optional: Delete index for a fresh start (use with caution in production)
        try:
            if PINECONE_INDEX_NAME in test_retriever_instance.pinecone_client.list_indexes():
                print(f"Deleting existing index '{PINECONE_INDEX_NAME}' for a fresh start...")
                test_retriever_instance.pinecone_client.delete_index(PINECONE_INDEX_NAME)
                print("Index deleted. Re-initializing client to create it again.")
                # Re-initialize the client to recreate the index
                test_retriever_instance._initialize_pinecone_client()
                if not test_retriever_instance.index:
                    print("Failed to re-initialize Pinecone client after deletion. Aborting.")
                    return
            else:
                print(f"Index '{PINECONE_INDEX_NAME}' does not exist, no need to delete.")
        except Exception as e:
            print(f"Error during index cleanup: {e}")
            # Continue even if cleanup fails, might be permission issue etc.

        source_url = "https://example.com/test_document.pdf"
        dummy_chunks = [
            "Artificial intelligence (AI) is intelligence demonstrated by machines.",
            "Machine learning (ML) is a subset of AI that focuses on the development of algorithms.",
            "Deep learning is a specialized subset of machine learning.",
            "Natural Language Processing (NLP) deals with the interaction between computers and human language.",
            "The capital of France is Paris.",
            "The Eiffel Tower is located in Paris."
        ]
        print(f"\nAdding {len(dummy_chunks)} dummy chunks...")
        success = await test_retriever_instance.add_document_chunks(dummy_chunks, source_url)
        if success:
            print("Dummy chunks added successfully.")
        else:
            print("Failed to add dummy chunks.")
            return

        time.sleep(5) # Give Pinecone a moment to index

        queries = [
            "What is machine learning?",
            "Tell me about AI.",
            "Where is the Eiffel Tower?"
        ]

        print("\nRetrieving chunks for queries:")
        for query_text in queries:
            print(f"\nQuery: '{query_text}'")
            retrieved = await test_retriever_instance.retrieve_relevant_chunks(query_text, top_k=2)
            if retrieved:
                print(f"Retrieved {len(retrieved)} chunks:")
                for i, chunk in enumerate(retrieved):
                    print(f"  Chunk {i+1}: {chunk}")
            else:
                print("No relevant chunks retrieved.")

        # Optional: Clean up after test by deleting the index
        try:
            if PINECONE_INDEX_NAME in test_retriever_instance.pinecone_client.list_indexes():
                print(f"\nDeleting index '{PINECONE_INDEX_NAME}' after test...")
                test_retriever_instance.pinecone_client.delete_index(PINECONE_INDEX_NAME)
                print("Index deleted.")
        except Exception as e:
            print(f"Error during post-test cleanup: {e}")

    asyncio.run(test_retriever_simple())
