from typing import Optional, List
from pydantic import BaseModel, Field

from app.schemas.extraction import ExtractedInformation, ClaimItem
from app.schemas.evidence import EvidenceItem, TechnicalObservation


class VerificationSummary(BaseModel):
    total_claims: int = Field(0, description="Total number of evaluated claims")
    supported: int = Field(0, description="Claims directly supported by available evidence")
    contradicted: int = Field(0, description="Claims directly contradicted by evidence")
    inconclusive: int = Field(0, description="Claims with partial or inconclusive technical observations")
    not_checked: int = Field(0, description="Claims that cannot be verified by technical checks alone")
    evidence_items: int = Field(0, description="Count of evidence artifacts collected")


class VerificationRequest(BaseModel):
    extracted_information: ExtractedInformation = Field(
        ..., description="Structured opportunity entities from Phase 2 extraction"
    )
    claims: List[ClaimItem] = Field(
        ..., description="List of extracted claims to cross-reference against evidence"
    )
    source_type: Optional[str] = Field("text", description="Origin source type (text, pdf, combined)")
    application_url: Optional[str] = Field(None, description="Optional submitted application URL")


class VerificationResponse(BaseModel):
    success: bool = Field(True, description="Verification pipeline execution status")
    verification_summary: VerificationSummary = Field(
        ..., description="Counts of claim verification states and evidence records"
    )
    claims: List[ClaimItem] = Field(
        ..., description="Claims updated with verification statuses, evidence IDs, and explanations"
    )
    evidence: List[EvidenceItem] = Field(
        default_factory=list, description="All independent technical evidence items collected"
    )
    technical_observations: List[TechnicalObservation] = Field(
        default_factory=list, description="Categorized technical observations (domain, DNS, email, URL)"
    )
    limitations: List[str] = Field(
        default_factory=list, description="Explicit system limitations and safety notices"
    )
    extracted_information: Optional[ExtractedInformation] = Field(
        None, description="Original opportunity information preserved for reference"
    )


class AnalyzeRequest(BaseModel):
    content: str = Field(
        ..., min_length=1, max_length=50000, description="Raw opportunity text or ingested document text"
    )
    source_type: Optional[str] = Field("text", description="Input type: text, pdf, combined")
    application_url: Optional[str] = Field(None, description="Optional submitted application URL")
    force_mode: Optional[str] = Field(
        None, description="Optional extraction override: 'ai' or 'rule_based'"
    )

