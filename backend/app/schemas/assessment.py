from typing import Optional, List, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field

from app.schemas.extraction import ExtractedInformation, ClaimItem
from app.schemas.evidence import EvidenceItem, TechnicalObservation
from app.schemas.verification import VerificationSummary, VerificationResponse


class AssessmentLevel(str, Enum):
    HIGH_CAUTION = "high_caution"
    NEEDS_CAREFUL_REVIEW = "needs_careful_review"
    LIMITED_CONCERNS_DETECTED = "limited_concerns_detected"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"


class FindingSeverity(str, Enum):
    INFORMATIONAL = "informational"
    CAUTION = "caution"
    HIGH_CAUTION = "high_caution"


class AssessmentFinding(BaseModel):
    finding_id: str = Field(..., description="Unique finding identifier, e.g. 'FND-001'")
    title: str = Field(..., description="Short finding title")
    severity: FindingSeverity = Field(..., description="Severity level: informational, caution, or high_caution")
    explanation: str = Field(..., description="Detailed factual explanation of the finding")
    related_claim_ids: List[str] = Field(default_factory=list, description="Claim IDs associated with this finding")
    related_evidence_ids: List[str] = Field(default_factory=list, description="Evidence IDs associated with this finding")
    why_it_matters: str = Field(..., description="Why this signal is significant for student decision-making")
    limitations: str = Field(..., description="What this finding does NOT prove or establish")
    recommended_action: str = Field(..., description="Recommended action for the candidate")


class SafetyRecommendation(BaseModel):
    recommendation_id: str = Field(..., description="Unique recommendation ID, e.g. 'REC-001'")
    topic: str = Field(..., description="Topic: payment_safety, recruiter_identity, domain_safety, personal_info, unverified_details")
    title: str = Field(..., description="Actionable recommendation headline")
    advice: str = Field(..., description="Specific step-by-step guidance")
    priority: int = Field(1, description="Priority rank (1 = immediate action, 2 = important check, 3 = good practice)")


class VerifiedFact(BaseModel):
    fact_id: str = Field(..., description="Unique fact identifier, e.g. 'FCT-001'")
    category: str = Field(..., description="Category: domain, dns, email, protocol")
    statement: str = Field(..., description="Objectively observed technical fact")
    source_name: str = Field(..., description="Authoritative source (RDAP, Cloudflare DoH, format analysis)")
    retrieved_at: str = Field(..., description="ISO 8601 timestamp of evidence retrieval")


class UnverifiedClaim(BaseModel):
    claim_id: str = Field(..., description="Associated claim identifier")
    category: str = Field(..., description="Claim category (financial, opportunity, recruiter, deadline)")
    statement: str = Field(..., description="The stated claim from the announcement")
    reason_unverified: str = Field(..., description="Why this claim cannot be verified by technical checks")


class NextStepItem(BaseModel):
    step_number: int = Field(..., description="Sequence number in prioritized checklist")
    action: str = Field(..., description="Specific action the student should take")
    rationale: str = Field(..., description="Why this step is critical before proceeding")


class AssessmentOverview(BaseModel):
    assessment_level: AssessmentLevel = Field(..., description="high_caution, needs_careful_review, limited_concerns_detected, insufficient_evidence")
    assessment_label: str = Field(..., description="Human-readable label for assessment category")
    summary: str = Field(..., description="Concise, explainable summary of the assessment")
    important_notice: str = Field(
        "This is an evidence-based assessment, not a guarantee of legitimacy or fraud. Never make financial or personal commitments based on unverified announcements.",
        description="Mandatory system safety notice"
    )


class AssessmentReport(BaseModel):
    assessment: AssessmentOverview = Field(..., description="Assessment category and overview summary")
    findings: List[AssessmentFinding] = Field(default_factory=list, description="Evidence-based reasoning findings")
    recommendations: List[SafetyRecommendation] = Field(default_factory=list, description="Prioritized safety recommendations")
    verified_facts: List[VerifiedFact] = Field(default_factory=list, description="Technical facts observed by external checks")
    unverified_claims: List[UnverifiedClaim] = Field(default_factory=list, description="Claims from announcement that remain unverified")
    limitations: List[str] = Field(default_factory=list, description="System methodology and evidence limitations")
    next_steps: List[NextStepItem] = Field(default_factory=list, description="Prioritized checklist for the student")


class AssessmentRequest(BaseModel):
    extracted_information: Optional[ExtractedInformation] = Field(None, description="Extracted entities")
    claims: List[ClaimItem] = Field(default_factory=list, description="Extracted claims")
    evidence: List[EvidenceItem] = Field(default_factory=list, description="Evidence items collected")
    technical_observations: List[TechnicalObservation] = Field(default_factory=list, description="Technical observations")
    verification_summary: Optional[VerificationSummary] = Field(None, description="Verification summary counts")
    limitations: List[str] = Field(default_factory=list, description="System limitations")
    # Support passing an entire VerificationResponse directly or nested
    verification_response: Optional[VerificationResponse] = Field(None, description="Optional nested verification response")

    def get_effective_data(self) -> Dict[str, Any]:
        if self.verification_response:
            vr = self.verification_response
            return {
                "extracted_information": vr.extracted_information,
                "claims": vr.claims,
                "evidence": vr.evidence,
                "technical_observations": vr.technical_observations,
                "verification_summary": vr.verification_summary,
                "limitations": vr.limitations,
            }
        return {
            "extracted_information": self.extracted_information,
            "claims": self.claims,
            "evidence": self.evidence,
            "technical_observations": self.technical_observations,
            "verification_summary": self.verification_summary,
            "limitations": self.limitations,
        }


class AssessmentResponse(BaseModel):
    success: bool = Field(True, description="Assessment execution status")
    assessment: AssessmentOverview = Field(..., description="Assessment category overview")
    findings: List[AssessmentFinding] = Field(default_factory=list, description="List of explainable findings")
    recommendations: List[SafetyRecommendation] = Field(default_factory=list, description="Contextual safety recommendations")
    verified_facts: List[VerifiedFact] = Field(default_factory=list, description="Independently verified technical facts")
    unverified_claims: List[UnverifiedClaim] = Field(default_factory=list, description="Claims that remain unverified")
    limitations: List[str] = Field(default_factory=list, description="Methodology limitations")
    next_steps: List[NextStepItem] = Field(default_factory=list, description="Actionable next steps")
    verification_summary: Optional[VerificationSummary] = Field(None, description="Verification summary")


class AnalysisResponse(VerificationResponse):
    assessment: AssessmentOverview = Field(..., description="Assessment category and overview")
    findings: List[AssessmentFinding] = Field(default_factory=list, description="Explainable findings")
    recommendations: List[SafetyRecommendation] = Field(default_factory=list, description="Contextual safety recommendations")
    verified_facts: List[VerifiedFact] = Field(default_factory=list, description="Independently verified technical facts")
    unverified_claims: List[UnverifiedClaim] = Field(default_factory=list, description="Claims that remain unverified")
    next_steps: List[NextStepItem] = Field(default_factory=list, description="Actionable next steps")

