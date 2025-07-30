import asyncio
from app.services.parser import document_parser

async def main():
    test_url = "https://arxiv.org/pdf/1706.03762.pdf"  # Known good test file

    print(f"Downloading from: {test_url}")
    text, content_type = await document_parser.parse_document(test_url)

    if text:
        print("✅ Document parsed successfully.")
        print(f"Content type: {content_type}")
        print(f"Extracted text (first 500 chars):\n{text[:500]}")
    else:
        print("❌ Failed to parse document.")
        print(f"Content type: {content_type}")

if __name__ == "__main__":
    asyncio.run(main())
