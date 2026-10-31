from fastapi import APIRouter, HTTPException, status
from app.schemas.verification import (
    VerificationRequest,
    VerificationResponse,
    AnalyzeRequest,
)
from app.services.verification_service import verification_service

router = APIRouter(prefix="/api/v1", tags=["Evidence & Verification"])


@router.post(
    "/verify",
    response_model=VerificationResponse,
    status_code=status.HTTP_200_OK,
    summary="Verify Opportunity Claims Against Technical Evidence",
)
async def verify_opportunity_claims(request: VerificationRequest) -> VerificationResponse:
    """
    Evaluates extracted opportunity claims against independent technical evidence:
    RDAP domain age/registration, DNS-over-HTTPS routing (A, AAAA, MX, NS, TXT),
    recruiter email-domain alignment, and URL structural security.
    Maps evidence to relevant claims without generating false fraud verdicts.
    """
    try:
        return await verification_service.verify(request)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Verification pipeline failed: {str(e)}",
        )


@router.post(
    "/analyze",
    response_model=VerificationResponse,
    status_code=status.HTTP_200_OK,
    summary="End-to-End Extraction & Evidence Verification",
)
async def analyze_opportunity_end_to_end(request: AnalyzeRequest) -> VerificationResponse:
    """
    Convenience endpoint: Ingests raw text, extracts structured entities and claims,
    and immediately performs independent evidence cross-referencing in a single request.
    """
    if not request.content or not request.content.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payload 'content' cannot be empty.",
        )
    try:
        return await verification_service.analyze(request)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"End-to-end analysis failed: {str(e)}",
        )
