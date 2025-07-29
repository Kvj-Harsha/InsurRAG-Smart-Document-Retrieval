# scripts/setup_schema.py

import weaviate
from weaviate.classes.init import Auth

# ✅ Hardcoded credentials (replace these securely later)
weaviate_url = "ufffwk4qsziqn0jd1bxdgq.c0.asia-southeast1.gcp.weaviate.cloud"
weaviate_api_key = "V0VTTzhhMFp1UndzTkVzRV9aenB5WVhLVFlDZWVDU1JlMDVMYksvVVFWR0tsVjMzTHN6bG1kTUNIeVpVPV92MjAw"

# 🌐 Connect to Weaviate Cloud
client = weaviate.connect_to_weaviate_cloud(
    cluster_url=weaviate_url,
    auth_credentials=Auth.api_key(weaviate_api_key),
)

# ✅ Create schema if it doesn't exist
if not client.schema.exists(class_name="DocumentChunk"):
    schema = {
        "class": "DocumentChunk",
        "description": "Text chunks",
        "properties": [
            {"name": "text", "dataType": ["text"]},
            {"name": "source", "dataType": ["string"]}
        ],
        "vectorizer": "none"
    }
    client.schema.create_class(schema)
    print("✅ Created DocumentChunk")
else:
    print("ℹ️ DocumentChunk already exists")

client.close()
