from fastapi import APIRouter, HTTPException, status
from app.schemas.verification import (
    VerificationRequest,
    VerificationResponse,
    AnalyzeRequest,
)
from app.schemas.assessment import (
    AssessmentRequest,
    AssessmentResponse,
    AnalysisResponse,
)
from app.services.verification_service import verification_service
from app.services.assessment_service import assessment_service

router = APIRouter(prefix="/api/v1", tags=["Verification & Assessment"])


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
    "/assess",
    response_model=AssessmentResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate Explainable Opportunity Assessment & Safety Guidance",
)
async def assess_opportunity(request: AssessmentRequest) -> AssessmentResponse:
    """
    Synthesizes extracted claims, technical observations, and evidence items into
    an explainable assessment report with deterministic categories (High caution,
    Needs careful review, Limited concerns detected, Insufficient evidence),
    actionable safety recommendations, and a prioritized next-steps checklist.
    """
    try:
        return assessment_service.assess(request)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Assessment generation failed: {str(e)}",
        )


@router.post(
    "/analyze",
    response_model=AnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="End-to-End Ingestion, Extraction, Verification & Assessment",
)
async def analyze_opportunity_end_to_end(request: AnalyzeRequest) -> AnalysisResponse:
    """
    Integrated pipeline:
    1. Ingests raw opportunity text or referenced application URL.
    2. Extracts structured entities, claims, and linguistic indicators.
    3. Gathers independent technical evidence (RDAP, DoH, Email, URL).
    4. Cross-references evidence with claims.
    5. Generates explainable assessment findings and guidance level.
    6. Produces contextual safety recommendations and next steps.
    Returns the complete, unified assessment report.
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
