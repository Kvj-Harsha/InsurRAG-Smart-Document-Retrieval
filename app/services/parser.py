import io
import httpx
import logging
from typing import Optional, Tuple
from PyPDF2 import PdfReader
from docx import Document as DocxDocument

from app.utils.config import settings

logger = logging.getLogger(__name__)

class DocumentParser:
    async def _download_document(self, url: str) -> Optional[bytes]:
        max_size = settings.MAX_DOCUMENT_SIZE_MB * 1024 * 1024
        try:
            async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
                logger.info(f"Downloading: {url}")
                response = await client.get(url)
                response.raise_for_status()

                downloaded = 0
                buffer = io.BytesIO()

                async for chunk in response.aiter_bytes():
                    downloaded += len(chunk)
                    if downloaded > max_size:
                        logger.warning("Download exceeded size limit.")
                        return None
                    buffer.write(chunk)

                logger.info(f"Downloaded {downloaded} bytes.")
                return buffer.getvalue()

        except Exception as e:
            logger.error(f"Download failed: {e}")
            return None

    def _parse_pdf(self, content: bytes) -> Optional[str]:
        try:
            reader = PdfReader(io.BytesIO(content))
            return "".join(page.extract_text() or "" for page in reader.pages)
        except Exception as e:
            logger.error(f"PDF parse error: {e}")
            return None

    def _parse_docx(self, content: bytes) -> Optional[str]:
        try:
            doc = DocxDocument(io.BytesIO(content))
            return "\n".join(p.text for p in doc.paragraphs)
        except Exception as e:
            logger.error(f"DOCX parse error: {e}")
            return None

    async def parse_document(self, url: str) -> Tuple[Optional[str], Optional[str]]:
        content = await self._download_document(url)
        if not content:
            return None, None

        if url.lower().endswith(".pdf"):
            return self._parse_pdf(content), "application/pdf"
        elif url.lower().endswith(".docx"):
            return self._parse_docx(content), "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

        return None, None

document_parser = DocumentParser()
