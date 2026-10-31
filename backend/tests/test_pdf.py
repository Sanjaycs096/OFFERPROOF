import io
import sys
from pathlib import Path
import pymupdf

backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from app.services.pdf_service import (
    extract_text_from_pdf,
    validate_pdf_bytes,
    PDFProcessingError,
    MAX_PDF_SIZE_BYTES,
    MAX_PDF_PAGES,
)


def create_sample_pdf(text: str = "Sample Offer Letter Text", num_pages: int = 1) -> bytes:
    """Helper to generate an in-memory PDF using PyMuPDF."""
    doc = pymupdf.open()
    for _ in range(num_pages):
        page = doc.new_page()
        if text:
            page.insert_text((50, 72), text)
    pdf_bytes = doc.tobytes()
    doc.close()
    return pdf_bytes


def test_valid_text_pdf():
    content = "Official Offer from Apex Corp. Position: Backend Intern. Stipend: $2,000/mo."
    pdf_bytes = create_sample_pdf(content)
    text, meta = extract_text_from_pdf(pdf_bytes, "offer.pdf")
    assert "Apex Corp" in text
    assert "Backend Intern" in text
    assert meta.filename == "offer.pdf"
    assert meta.page_count == 1
    assert meta.file_size_bytes == len(pdf_bytes)
    print("[PASS] Valid text PDF extraction passed.")


def test_empty_pdf_raises_error():
    """An empty PDF with no text should raise PDFProcessingError."""
    pdf_bytes = create_sample_pdf(text="", num_pages=1)
    try:
        extract_text_from_pdf(pdf_bytes, "empty.pdf")
        assert False, "Expected PDFProcessingError for empty PDF"
    except PDFProcessingError as e:
        assert "No selectable text found" in str(e)
        print("[PASS] Empty PDF rejection passed:", str(e)[:45])


def test_invalid_header_raises_error():
    """Non-PDF binary signature should be rejected immediately."""
    fake_bytes = b"NOT_A_PDF_FILE_HEADER_XYZ"
    try:
        validate_pdf_bytes(fake_bytes, "fake.pdf")
        assert False, "Expected PDFProcessingError for invalid magic bytes"
    except PDFProcessingError as e:
        assert "valid PDF signature" in str(e)
        print("[PASS] Invalid signature rejection passed.")


def test_oversized_pdf_raises_error():
    """Files exceeding size limit must be rejected."""
    fake_large = b"%PDF-" + (b"0" * (MAX_PDF_SIZE_BYTES + 10))
    try:
        validate_pdf_bytes(fake_large, "huge.pdf")
        assert False, "Expected PDFProcessingError for large file"
    except PDFProcessingError as e:
        assert "exceeds maximum allowed limit" in str(e)
        print("[PASS] Oversized PDF rejection passed.")


def test_page_limit_enforced():
    """PDFs exceeding 15 pages should be rejected."""
    multi_page_pdf = create_sample_pdf("Page content", num_pages=MAX_PDF_PAGES + 2)
    try:
        extract_text_from_pdf(multi_page_pdf, "long.pdf")
        assert False, "Expected PDFProcessingError for exceeding max pages"
    except PDFProcessingError as e:
        assert "exceeds maximum page limit" in str(e)
        print("[PASS] Page count limit enforcement passed.")


if __name__ == "__main__":
    test_valid_text_pdf()
    test_empty_pdf_raises_error()
    test_invalid_header_raises_error()
    test_oversized_pdf_raises_error()
    test_page_limit_enforced()
    print("\nALL PDF TESTS PASSED!")
