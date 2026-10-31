from typing import Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from app.schemas.ingestion import (
    TextIngestRequest,
    IngestResponse,
)
from app.schemas.extraction import (
    ExtractionRequest,
    ExtractionResponse,
)
from app.services.ingestion_service import (
    ingest_text_content,
    ingest_pdf_content,
)
from app.services.pdf_service import (
    PDFProcessingError,
    MAX_PDF_SIZE_BYTES,
)
from app.services.extraction_service import extraction_service
from app.services.ai_service import get_ai_provider

router = APIRouter(prefix="/api/v1", tags=["Ingestion & Extraction"])


@router.get("/health", summary="API v1 Health & Capabilities")
def api_v1_health():
    """
    Returns API v1 system status, ingestion capability flags, evidence verification status, and AI provider status.
    """
    ai_provider = get_ai_provider()
    return {
        "status": "ok",
        "api_version": "v1",
        "features": {
            "text_ingestion": True,
            "pdf_ingestion": True,
            "claim_extraction": True,
            "rule_based_fallback": True,
            "evidence_verification": True,
            "rdap_intelligence": True,
            "dns_over_https": True,
            "email_domain_consistency": True,
            "ai_extraction_configured": ai_provider.is_configured,
            "ai_provider": ai_provider.provider_name if ai_provider.is_configured else "none",
        },
    }


@router.post(
    "/ingest/text",
    response_model=IngestResponse,
    status_code=status.HTTP_200_OK,
    summary="Ingest Raw Opportunity Text",
)
def ingest_text(request: TextIngestRequest) -> IngestResponse:
    """
    Ingests pasted opportunity text, sanitizes content, and extracts reference URL metadata.
    """
    try:
        return ingest_text_content(request)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred during text ingestion: {str(e)}",
        )


@router.post(
    "/ingest/pdf",
    response_model=IngestResponse,
    status_code=status.HTTP_200_OK,
    summary="Ingest PDF Opportunity Document",
)
async def ingest_pdf(
    file: UploadFile = File(..., description="PDF document of the job or offer letter"),
    url: Optional[str] = Form(None, description="Optional application or listing URL reference"),
) -> IngestResponse:
    """
    Uploads a text-based PDF document, validates size and signature, extracts text via PyMuPDF in memory,
    and returns sanitized text and document metadata.
    """
    filename = file.filename or "uploaded_document.pdf"

    # Quick MIME check if provided
    if file.content_type and "pdf" not in file.content_type.lower() and not filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported file format: Only PDF documents (.pdf) are accepted.",
        )

    try:
        # Read file into memory (enforcing size check before buffering large chunks)
        contents = await file.read()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to read uploaded file: {str(e)}",
        )

    if len(contents) > MAX_PDF_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File exceeds maximum allowed limit of {MAX_PDF_SIZE_BYTES // (1024 * 1024)} MB.",
        )

    try:
        return ingest_pdf_content(file_bytes=contents, filename=filename, url=url)
    except PDFProcessingError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred during PDF parsing: {str(e)}",
        )


@router.post(
    "/extract",
    response_model=ExtractionResponse,
    status_code=status.HTTP_200_OK,
    summary="Extract Structured Entities & Verifiable Claims",
)
async def extract_claims_and_entities(request: ExtractionRequest) -> ExtractionResponse:
    """
    Processes opportunity text, performs AI extraction (or deterministic rule-based fallback),
    isolates claims, categorizes entities, and flags suspicious language patterns.
    All claims are returned with verification_status='not_checked'.
    """
    if not request.content or not request.content.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Extraction payload 'content' cannot be empty.",
        )

    try:
        return await extraction_service.extract(request)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Extraction failed: {str(e)}",
        )
