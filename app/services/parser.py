import io
import httpx
import logging
from typing import Optional, Tuple
from urllib.parse import urlparse

from PyPDF2 import PdfReader
from docx import Document as DocxDocument
from email import message_from_bytes
from bs4 import BeautifulSoup

from app.utils.config import settings

logger = logging.getLogger(__name__)


class DocumentParser:
    async def _download_document(self, url: str) -> Optional[Tuple[bytes, str]]:
        max_size = settings.MAX_DOCUMENT_SIZE_MB * 1024 * 1024
        try:
            async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
                logger.info(f"Downloading: {url}")
                response = await client.get(url)
                response.raise_for_status()

                content_type = response.headers.get("Content-Type", "").lower()
                logger.info(f"Detected Content-Type: {content_type}")

                downloaded = 0
                buffer = io.BytesIO()

                async for chunk in response.aiter_bytes():
                    downloaded += len(chunk)
                    if downloaded > max_size:
                        logger.warning("Download exceeded size limit.")
                        return None
                    buffer.write(chunk)

                logger.info(f"Downloaded {downloaded} bytes.")
                return buffer.getvalue(), content_type

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

    def _parse_eml(self, content: bytes) -> Optional[str]:
        try:
            msg = message_from_bytes(content)

            subject = msg.get("Subject", "")
            sender = msg.get("From", "")
            to = msg.get("To", "")
            date = msg.get("Date", "")

            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    if content_type == "text/plain":
                        body = part.get_payload(decode=True).decode(errors="ignore")
                        break
                    elif content_type == "text/html":
                        html = part.get_payload(decode=True).decode(errors="ignore")
                        body = BeautifulSoup(html, "html.parser").get_text()
                        break
            else:
                body = msg.get_payload(decode=True).decode(errors="ignore")

            combined = f"Subject: {subject}\nFrom: {sender}\nTo: {to}\nDate: {date}\n\n{body}"
            return combined.strip()
        except Exception as e:
            logger.error(f"EML parse error: {e}")
            return None

    def _infer_extension(self, url: str, content_type: str) -> str:
        parsed = urlparse(url)
        full_path = parsed.path + parsed.query

        if ".pdf" in full_path.lower() or "application/pdf" in content_type:
            return "pdf"
        if ".docx" in full_path.lower() or "application/vnd.openxmlformats-officedocument.wordprocessingml.document" in content_type:
            return "docx"
        if ".eml" in full_path.lower() or "message/rfc822" in content_type:
            return "eml"
        return "unknown"

    async def parse_document(self, url: str) -> Tuple[Optional[str], Optional[str]]:
        result = await self._download_document(url)
        if not result:
            return None, None

        content, content_type = result
        file_type = self._infer_extension(url, content_type)

        if file_type == "pdf":
            return self._parse_pdf(content), "application/pdf"
        elif file_type == "docx":
            return self._parse_docx(content), "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        elif file_type == "eml":
            return self._parse_eml(content), "message/rfc822"

        logger.warning(f"❌ Unable to determine document type for: {url}")
        return None, None


document_parser = DocumentParser()
