from typing import Optional, List, Dict, Any, Literal
from pydantic import BaseModel, Field
from app.schemas.ingestion import UrlMetadata


class OrganisationInfo(BaseModel):
    name: Optional[str] = Field(None, description="Extracted organisation / company name")
    website: Optional[str] = Field(None, description="Organisation official domain or website")
    organisation_type: Optional[str] = Field(
        None, description="Category of entity, e.g. company, university, agency, ngo"
    )


class OpportunityInfo(BaseModel):
    title: Optional[str] = Field(None, description="Opportunity title or headline")
    category: Optional[str] = Field(
        None, description="Classification: job, internship, scholarship, fellowship, other"
    )
    role: Optional[str] = Field(None, description="Specific job role or title")
    required_qualifications: List[str] = Field(
        default_factory=list, description="Extracted degrees, prerequisites, or requirements"
    )
    required_skills: List[str] = Field(
        default_factory=list, description="Extracted skills or competencies"
    )
    work_arrangement: Optional[str] = Field(
        None, description="Working setup: remote, onsite, hybrid, not_specified"
    )
    location: Optional[str] = Field(None, description="Job or opportunity physical location")
    duration: Optional[str] = Field(None, description="Program or employment duration")
    application_deadline: Optional[str] = Field(
        None, description="Stated application deadline or expiry date"
    )


class FinancialDetails(BaseModel):
    salary: Optional[str] = Field(None, description="Advertised salary or compensation")
    stipend: Optional[str] = Field(None, description="Advertised stipend for internship/fellowship")
    registration_fees: Optional[str] = Field(
        None, description="Demanded registration fees, preserving original currency/symbol"
    )
    training_fees: Optional[str] = Field(None, description="Demanded training / material fees")
    processing_fees: Optional[str] = Field(None, description="Demanded application / visa / processing fees")
    other_payment_requests: List[str] = Field(
        default_factory=list, description="Other demanded payments, deposits, or purchases"
    )


class RecruiterInfo(BaseModel):
    name: Optional[str] = Field(None, description="Contact recruiter or sender name")
    email: Optional[str] = Field(None, description="Recruiter contact email address")
    phone: Optional[str] = Field(None, description="Recruiter telephone or WhatsApp number")
    contact_info: Optional[str] = Field(
        None, description="Recruiter social or messaging handles (Telegram, LinkedIn, etc.)"
    )


class ApplicationInfo(BaseModel):
    application_url: Optional[str] = Field(None, description="Direct application or portal link")
    application_email: Optional[str] = Field(None, description="Destination email for resumes")
    application_instructions: Optional[str] = Field(
        None, description="Key steps or procedures instructed for candidates"
    )


class ExtractedInformation(BaseModel):
    organisation: OrganisationInfo = Field(default_factory=OrganisationInfo)
    opportunity: OpportunityInfo = Field(default_factory=OpportunityInfo)
    financial_details: FinancialDetails = Field(default_factory=FinancialDetails)
    recruiter: RecruiterInfo = Field(default_factory=RecruiterInfo)
    application: ApplicationInfo = Field(default_factory=ApplicationInfo)


class ClaimItem(BaseModel):
    claim_id: str = Field(..., description="Unique claim identifier (e.g. CLM-001)")
    claim_text: str = Field(..., description="Formal claim statement drawn from submitted text")
    claim_category: str = Field(
        ...,
        description="Category: organisation, opportunity, financial, deadline, requirement, recruiter, suspicious_indicator",
    )
    extracted_value: Optional[str] = Field(
        None, description="Specific extracted value or claim subject"
    )
    source_text: str = Field(..., description="Verbatim supporting text span from the input")
    source_position: Optional[Dict[str, int]] = Field(
        None, description="Start and end character offsets in the input text"
    )
    confidence: float = Field(
        0.8, ge=0.0, le=1.0, description="Extraction confidence score from 0.0 to 1.0"
    )
    verification_status: Literal["supported", "contradicted", "inconclusive", "not_checked"] = Field(
        "not_checked",
        description="Verification state: supported, contradicted, inconclusive, or not_checked",
    )
    evidence_ids: List[str] = Field(
        default_factory=list,
        description="IDs of evidence items associated with this claim (e.g. EVD-001)",
    )
    verification_explanation: Optional[str] = Field(
        None,
        description="Plain-language explanation of the evidence basis for the verification status",
    )


class SuspiciousIndicator(BaseModel):
    indicator_type: str = Field(
        ...,
        description="Type: guaranteed_selection, registration_fee, urgent_payment, unrealistic_compensation, unauthenticated_channel, sensitive_info_request, artificial_urgency",
    )
    statement: str = Field(..., description="Identified suspicious statement or phrase")
    description: str = Field(
        ..., description="Explanation of why this statement is recognized as a pattern"
    )
    source_quote: Optional[str] = Field(None, description="Direct quote from the input")


class ExtractionSummary(BaseModel):
    total_claims: int = Field(0, description="Count of extracted individual claims")
    total_entities: int = Field(0, description="Count of populated entity fields")
    detected_indicators: int = Field(0, description="Count of flagged language indicators")


class ExtractionRequest(BaseModel):
    content: str = Field(
        ..., min_length=1, max_length=50000, description="Raw opportunity text or ingested document text"
    )
    source_type: Optional[str] = Field("text", description="Input type: text, pdf, combined")
    application_url: Optional[str] = Field(None, description="Optional submitted application URL")
    force_mode: Optional[str] = Field(
        None, description="Optional override: 'ai' or 'rule_based'. Defaults to auto (AI if configured)."
    )


class ExtractionResponse(BaseModel):
    success: bool = Field(True, description="Extraction operation success indicator")
    extraction_mode: Literal["ai", "rule_based"] = Field(
        ..., description="Extraction engine mode: 'ai' (LLM structured) or 'rule_based' (deterministic)"
    )
    source_type: str = Field(..., description="Medium of processed source")
    extracted_information: ExtractedInformation = Field(
        default_factory=ExtractedInformation, description="Hierarchical extracted opportunity details"
    )
    claims: List[ClaimItem] = Field(
        default_factory=list, description="Extracted individual verifiable claims"
    )
    suspicious_indicators: List[SuspiciousIndicator] = Field(
        default_factory=list, description="Extracted suspicious language indicators"
    )
    extraction_summary: ExtractionSummary = Field(
        default_factory=ExtractionSummary, description="Aggregation counts of claims and entities"
    )
    url_metadata: Optional[UrlMetadata] = Field(
        None, description="Parsed application URL metadata if provided"
    )
    errors: Optional[List[str]] = Field(None, description="Any non-fatal operational notices")
