from pinecone import Pinecone, ServerlessSpec
from app.utils.config import settings

# Initialize Pinecone client
pc = Pinecone(api_key=settings.PINECONE_API_KEY)

# Check if the index already exists before creating
index_name = settings.PINECONE_INDEX_NAME

if index_name not in [index.name for index in pc.list_indexes()]:
    pc.create_index(
        name=index_name,
        dimension=settings.NOMIC_EMBED_DIMENSION,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-west-2"
        )
    )

# Connect to the index
index = pc.Index(index_name)
