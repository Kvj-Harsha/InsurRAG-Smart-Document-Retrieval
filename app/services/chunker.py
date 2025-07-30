from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.services.parser import document_parser

# Tweak these depending on your RAG setup
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

def chunk_text(text: str) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    return splitter.split_text(text)

async def chunk_from_url(document_url: str) -> list[str]:
    """
    Parses a document from the given URL and returns a list of text chunks.
    """
    text, _ = await document_parser.parse_document(document_url)
    if not text:
        raise ValueError(f"Failed to parse or extract content from: {document_url}")

    return chunk_text(text)
