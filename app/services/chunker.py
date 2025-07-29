# app/services/chunker.py

from langchain.text_splitter import RecursiveCharacterTextSplitter

# You can tweak these depending on performance & model size
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

def chunk_text(text: str) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    return splitter.split_text(text)
