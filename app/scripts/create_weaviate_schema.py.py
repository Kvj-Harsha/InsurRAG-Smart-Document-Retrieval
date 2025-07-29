# scripts/create_weaviate_schema.py

schema = {
    "class": "DocumentChunk",
    "description": "Chunked text from uploaded documents",
    "vectorizer": "none",
    "properties": [
        {"name": "text", "dataType": ["text"]},
        {"name": "doc_id", "dataType": ["string"]},
        {"name": "chunk_id", "dataType": ["string"]}
    ]
}
