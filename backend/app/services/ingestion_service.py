import re
from urllib.parse import urlparse
from typing import Optional, Tuple
from app.schemas.ingestion import UrlMetadata, TextIngestRequest, IngestResponse
from app.services.pdf_service import extract_text_from_pdf

MAX_TEXT_LENGTH = 50000


def parse_url_metadata(raw_url: Optional[str]) -> Optional[UrlMetadata]:
    """
    Safely parses URL structural information without issuing external network requests.
    Prevents SSRF and unauthorized external connections during ingestion.
    """
    if not raw_url or not raw_url.strip():
        return None

    cleaned_url = raw_url.strip()
    if not (cleaned_url.startswith("http://") or cleaned_url.startswith("https://")):
        cleaned_url = "https://" + cleaned_url

    try:
        parsed = urlparse(cleaned_url)
        hostname = parsed.hostname.lower() if parsed.hostname else None
        return UrlMetadata(
            submitted_url=raw_url.strip(),
            hostname=hostname,
            scheme=parsed.scheme or "https",
            path=parsed.path if parsed.path else "/",
        )
    except Exception:
        return UrlMetadata(
            submitted_url=raw_url.strip(),
            hostname=None,
            scheme=None,
            path=None,
        )


def sanitize_input_text(raw_text: str) -> str:
    """
    Sanitizes raw text, strips null bytes and normalizing line endings.
    """
    if not raw_text:
        return ""

    # Remove null bytes and control chars (except standard whitespace/newlines)
    sanitized = raw_text.replace("\x00", "")
    sanitized = re.sub(r"[\r\n]+", "\n", sanitized)
    sanitized = sanitized.strip()

    if len(sanitized) > MAX_TEXT_LENGTH:
        sanitized = sanitized[:MAX_TEXT_LENGTH]

    return sanitized


def ingest_text_content(request: TextIngestRequest) -> IngestResponse:
    """
    Processes pasted text and optional URL reference.
    """
    cleaned_text = sanitize_input_text(request.text)
    if not cleaned_text:
        raise ValueError("Submitted text is empty or contains only whitespace.")

    url_meta = parse_url_metadata(request.url)

    return IngestResponse(
        success=True,
        source_type="text",
        content=cleaned_text,
        content_length=len(cleaned_text),
        url_metadata=url_meta,
        document_metadata=None,
        message=f"Successfully ingested {len(cleaned_text)} characters of text.",
    )


def ingest_pdf_content(file_bytes: bytes, filename: str, url: Optional[str] = None) -> IngestResponse:
    """
    Processes uploaded PDF bytes in memory and extracts text.
    """
    text, doc_metadata = extract_text_from_pdf(file_bytes, filename)
    cleaned_text = sanitize_input_text(text)
    url_meta = parse_url_metadata(url)

    return IngestResponse(
        success=True,
        source_type="pdf",
        content=cleaned_text,
        content_length=len(cleaned_text),
        url_metadata=url_meta,
        document_metadata=doc_metadata,
        message=f"Successfully extracted {len(cleaned_text)} characters from {doc_metadata.page_count} PDF pages.",
    )
