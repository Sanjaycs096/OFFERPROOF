import io
import pymupdf
from typing import Tuple, Dict, Any, Optional
from app.schemas.ingestion import DocumentMetadata

MAX_PDF_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB
MAX_PDF_PAGES = 15
PDF_MAGIC_BYTES = b"%PDF-"


class PDFProcessingError(Exception):
    """Custom exception for PDF validation and parsing errors."""
    pass


def validate_pdf_bytes(file_bytes: bytes, filename: str) -> None:
    """
    Validates file size and PDF magic bytes.
    """
    if len(file_bytes) == 0:
        raise PDFProcessingError("Uploaded file is empty (0 bytes).")

    if len(file_bytes) > MAX_PDF_SIZE_BYTES:
        raise PDFProcessingError(
            f"File size exceeds maximum allowed limit of {MAX_PDF_SIZE_BYTES // (1024 * 1024)} MB."
        )

    # Magic byte check
    if not file_bytes.startswith(PDF_MAGIC_BYTES):
        raise PDFProcessingError(
            "Invalid file format: File does not possess valid PDF signature header (%PDF-)."
        )


def extract_text_from_pdf(file_bytes: bytes, filename: str) -> Tuple[str, DocumentMetadata]:
    """
    Extracts text from PDF bytes using PyMuPDF in memory.
    Enforces page limit and detects empty / image-only PDFs.
    """
    validate_pdf_bytes(file_bytes, filename)

    try:
        # Open PDF from memory stream
        doc = pymupdf.open(stream=file_bytes, filetype="pdf")
    except Exception as e:
        raise PDFProcessingError(f"Failed to parse PDF document structure: {str(e)}")

    try:
        page_count = len(doc)
        if page_count == 0:
            raise PDFProcessingError("PDF document contains 0 pages.")

        if page_count > MAX_PDF_PAGES:
            raise PDFProcessingError(
                f"PDF exceeds maximum page limit of {MAX_PDF_PAGES} pages (found {page_count} pages)."
            )

        extracted_text_pages = []
        for page_num in range(page_count):
            page = doc[page_num]
            page_text = page.get_text("text") or ""
            extracted_text_pages.append(page_text.strip())

        full_text = "\n\n".join(t for t in extracted_text_pages if t).strip()

        # Handle empty or image-only PDFs gracefully
        if not full_text:
            raise PDFProcessingError(
                "No selectable text found in the PDF. The document may be empty, password-protected, "
                "or contain only scanned images/photos. Phase 2 requires text-based PDF documents."
            )

        metadata_dict = doc.metadata or {}
        doc_metadata = DocumentMetadata(
            filename=filename,
            file_size_bytes=len(file_bytes),
            page_count=page_count,
            title=metadata_dict.get("title") or None,
            author=metadata_dict.get("author") or None,
        )

        return full_text, doc_metadata
    finally:
        doc.close()
