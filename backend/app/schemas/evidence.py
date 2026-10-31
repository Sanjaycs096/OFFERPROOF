from datetime import datetime, timezone
from typing import Optional, List, Dict, Any, Literal
from pydantic import BaseModel, Field

EvidenceStatus = Literal["available", "not_available", "error", "not_applicable"]


class EvidenceItem(BaseModel):
    evidence_id: str = Field(..., description="Unique evidence identifier, e.g. EVD-001")
    evidence_type: str = Field(
        ...,
        description="Type of evidence: domain_registration, dns_records, email_domain_consistency, url_consistency, organisation_consistency",
    )
    source_name: str = Field(..., description="Evidence data source, e.g. RDAP, DNS-over-HTTPS, Structural URL Analysis")
    source_url: Optional[str] = Field(None, description="Actual provider query URL when available")
    observed_value: str = Field(..., description="Primary observation or summary string")
    interpretation: str = Field(..., description="Plain-language explanation of what this observation means")
    retrieved_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="ISO 8601 UTC timestamp of retrieval",
    )
    status: EvidenceStatus = Field(..., description="Status: available, not_available, error, not_applicable")
    limitations: List[str] = Field(
        default_factory=list,
        description="Explicit limitations and what this check cannot establish",
    )
    raw_data: Optional[Dict[str, Any]] = Field(
        None, description="Structured raw observations for transparency"
    )


class TechnicalObservation(BaseModel):
    observation_id: str = Field(..., description="Unique observation ID, e.g. OBS-001")
    category: Literal["domain", "dns", "email", "url", "organisation"] = Field(
        ..., description="Observation category"
    )
    label: str = Field(..., description="Human-readable label, e.g. 'Recent domain registration'")
    finding: str = Field(
        ...,
        description="Standardized finding code: matching_domain, different_domain, free_email_provider, recent_domain, established_domain, new_domain, unknown_age, has_mx, no_mx, https, http_only, etc.",
    )
    detail: str = Field(..., description="Detailed description of the observation")
    severity: Literal["neutral", "informational", "notable"] = Field(
        "informational", description="Significance level of the observation"
    )
