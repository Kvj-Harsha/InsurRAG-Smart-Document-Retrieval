from pinecone import Pinecone
import uuid

# Initialize Pinecone client with correct environment
pc = Pinecone(
    api_key="pcsk_3oQZ3R_7gfF8EfnTNMVJ3vGMFDY2vi2B9aMcxvU4opDPH1KboDVq2N5d3BCpeMY8QJj5XK",
    environment="us-east-1-aws"
)

# Connect to existing index
index = pc.Index("bajaj")

# Create a dummy embedding vector (768-dim, all ones)
vector = [1.0] * 768

# Insert a vector with a random ID
vector_id = f"test-vector-{uuid.uuid4().hex[:8]}"
index.upsert([
    {
        "id": vector_id,
        "values": vector,
        "metadata": {
            "content": "This is a test vector inserted from script.",
            "source": "script"
        }
    }
])

print(f"Inserted test vector with ID: {vector_id}")
