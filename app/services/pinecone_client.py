from pinecone import Pinecone, ServerlessSpec
from app.utils.config import settings

# Initialize Pinecone client
pc = Pinecone(api_key=settings.PINECONE_API_KEY)

# Index name from your settings
index_name = settings.PINECONE_INDEX_NAME

# Use correct dimension for your local model
embedding_dimension = 384  # ← change from NOMIC_EMBED_DIMENSION

# Check if index already exists
if index_name not in [index.name for index in pc.list_indexes()]:
    pc.create_index(
        name=index_name,
        dimension=embedding_dimension,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

# Connect to the index
index = pc.Index(index_name)
