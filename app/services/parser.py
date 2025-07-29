import io
import httpx
import logging
from typing import Optional, Tuple
from PyPDF2 import PdfReader # Corrected import statement
from docx import Document as DocxDocument # Renamed to avoid conflict with 'documents' param

from app.utils.config import settings
from app.utils.logger import setup_logging # Ensure logging is set up

# Get a logger instance for this module
logger = logging.getLogger(__name__)

class DocumentParser:
    """
    Handles downloading documents from URLs and parsing their text content.
    Supports PDF and DOCX formats.
    """

    async def _download_document(self, url: str) -> Optional[bytes]:
        """
        Asynchronously downloads a document from the given URL.
        Handles potential network errors and large file sizes.
        """
        max_size_bytes = settings.MAX_DOCUMENT_SIZE_MB * 1024 * 1024
        try:
            # Use httpx for asynchronous HTTP requests
            async with httpx.AsyncClient() as client:
                logger.info(f"Attempting to download document from: {url}")
                response = await client.get(url, follow_redirects=True, timeout=30.0)
                response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)

                # Check content length if available, or stream to check size
                content_length = response.headers.get('content-length')
                if content_length and int(content_length) > max_size_bytes:
                    logger.warning(f"Document at {url} is too large ({content_length} bytes). Max allowed: {max_size_bytes} bytes.")
                    return None

                # If content-length is not available, or for safety, read in chunks
                # to prevent loading excessively large files into memory
                downloaded_size = 0
                content_buffer = io.BytesIO()
                async for chunk in response.aiter_bytes():
                    downloaded_size += len(chunk)
                    if downloaded_size > max_size_bytes:
                        logger.warning(f"Document at {url} exceeded max size during download. Aborting.")
                        return None
                    content_buffer.write(chunk)

                logger.info(f"Successfully downloaded document from: {url} (Size: {downloaded_size} bytes)")
                return content_buffer.getvalue()

        except httpx.RequestError as e:
            logger.error(f"Network error downloading document from {url}: {e}")
            return None
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error downloading document from {url}: {e.response.status_code} - {e.response.text}")
            return None
        except Exception as e:
            logger.error(f"An unexpected error occurred during document download from {url}: {e}")
            return None

    def _parse_pdf(self, file_content: bytes) -> Optional[str]:
        """
        Parses text content from a PDF file.
        """
        try:
            # PdfReader expects a file-like object
            pdf_file = io.BytesIO(file_content)
            reader = PdfReader(pdf_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or "" # extract_text can return None
            logger.info("Successfully parsed PDF document.")
            return text
        except Exception as e:
            logger.error(f"Error parsing PDF document: {e}")
            return None

    def _parse_docx(self, file_content: bytes) -> Optional[str]:
        """
        Parses text content from a DOCX file.
        """
        try:
            docx_file = io.BytesIO(file_content)
            document = DocxDocument(docx_file)
            text = "\n".join([paragraph.text for paragraph in document.paragraphs])
            logger.info("Successfully parsed DOCX document.")
            return text
        except Exception as e:
            logger.error(f"Error parsing DOCX document: {e}")
            return None

    async def parse_document(self, document_url: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Downloads and parses a document from the given URL.
        Returns the extracted text and the detected content type.
        """
        file_content = await self._download_document(document_url)
        if not file_content:
            return None, None

        # Simple content type detection based on URL extension
        # In a real-world scenario, you might use python-magic or inspect HTTP headers
        # for more robust content type detection.
        content_type: Optional[str] = None
        if document_url.lower().endswith(".pdf"):
            content_type = "application/pdf"
            parsed_text = self._parse_pdf(file_content)
        elif document_url.lower().endswith(".docx"):
            content_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            parsed_text = self._parse_docx(file_content)
        else:
            logger.warning(f"Unsupported document type for URL: {document_url}")
            return None, None

        if parsed_text is None:
            logger.error(f"Failed to parse document from URL: {document_url}")
            return None, content_type

        return parsed_text, content_type

# Instantiate the parser for use in other modules
document_parser = DocumentParser()
