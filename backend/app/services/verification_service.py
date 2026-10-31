import logging
import asyncio
from typing import List, Dict, Any, Optional

from app.schemas.extraction import ClaimItem, ExtractionRequest
from app.schemas.evidence import EvidenceItem, TechnicalObservation
from app.schemas.verification import (
    VerificationRequest,
    VerificationResponse,
    VerificationSummary,
    AnalyzeRequest,
)
from app.services.evidence import (
    VerificationContext,
    BaseEvidenceProvider,
    DomainIntelligenceProvider,
    DNSIntelligenceProvider,
    EmailDomainConsistencyProvider,
    URLConsistencyProvider,
    OrganisationIdentityConsistencyProvider,
)
from app.services.extraction_service import extraction_service

logger = logging.getLogger(__name__)

SYSTEM_VERIFICATION_LIMITATIONS = [
    "Technical checks evaluate domain, DNS, protocol, and email consistency. They cannot establish whether an opportunity or recruiter is genuine.",
    "The presence of active DNS or HTTPS indicates technical network routing, NOT organisational honesty or employment legitimacy.",
    "Authoritative government corporate registry records (e.g. SEC EDGAR, Companies House, MCA) are not queried in Phase 3; organisation incorporation remains unverified.",
    "Financial claims (salaries, stipends, demanded registration fees), application deadlines, and job offers cannot be verified via DNS or RDAP records and remain strictly 'not_checked'.",
    "In accordance with strict security standards, submitted websites were not visited, downloaded, or scraped."
]


class VerificationService:
    def __init__(self, providers: Optional[List[BaseEvidenceProvider]] = None):
        self.providers = providers or [
            DomainIntelligenceProvider(),
            DNSIntelligenceProvider(),
            EmailDomainConsistencyProvider(),
            URLConsistencyProvider(),
            OrganisationIdentityConsistencyProvider(),
        ]

    async def verify(self, request: VerificationRequest) -> VerificationResponse:
        context = VerificationContext(
            extracted_information=request.extracted_information,
            application_url=request.application_url,
        )

        # Collect evidence concurrently from all providers
        provider_tasks = [provider.collect(context) for provider in self.providers]
        provider_results = await asyncio.gather(*provider_tasks, return_exceptions=True)

        all_evidence: List[EvidenceItem] = []
        all_observations: List[TechnicalObservation] = []

        for res in provider_results:
            if isinstance(res, tuple) and len(res) == 2:
                ev_items, obs_items = res
                all_evidence.extend(ev_items)
                all_observations.extend(obs_items)
            elif isinstance(res, Exception):
                logger.error(f"Evidence provider encountered unexpected error: {type(res).__name__}: {str(res)}")

        # Map evidence to claims
        updated_claims = self._map_evidence_to_claims(request.claims, all_evidence, all_observations, context)

        # Compute summary
        supported_count = sum(1 for c in updated_claims if c.verification_status == "supported")
        contradicted_count = sum(1 for c in updated_claims if c.verification_status == "contradicted")
        inconclusive_count = sum(1 for c in updated_claims if c.verification_status == "inconclusive")
        not_checked_count = sum(1 for c in updated_claims if c.verification_status == "not_checked")

        summary = VerificationSummary(
            total_claims=len(updated_claims),
            supported=supported_count,
            contradicted=contradicted_count,
            inconclusive=inconclusive_count,
            not_checked=not_checked_count,
            evidence_items=len(all_evidence),
        )

        return VerificationResponse(
            success=True,
            verification_summary=summary,
            claims=updated_claims,
            evidence=all_evidence,
            technical_observations=all_observations,
            limitations=SYSTEM_VERIFICATION_LIMITATIONS,
            extracted_information=request.extracted_information,
        )

    async def analyze(self, request: AnalyzeRequest) -> VerificationResponse:
        """
        Convenience workflow: runs Phase 2 claim extraction first,
        followed immediately by Phase 3 evidence verification.
        """
        extract_req = ExtractionRequest(
            content=request.content,
            source_type=request.source_type or "text",
            application_url=request.application_url,
            force_mode=request.force_mode,
        )
        extraction_res = await extraction_service.extract(extract_req)

        verify_req = VerificationRequest(
            extracted_information=extraction_res.extracted_information,
            claims=extraction_res.claims,
            source_type=extraction_res.source_type,
            application_url=request.application_url,
        )
        return await self.verify(verify_req)

    def _map_evidence_to_claims(
        self,
        claims: List[ClaimItem],
        evidence: List[EvidenceItem],
        observations: List[TechnicalObservation],
        context: VerificationContext,
    ) -> List[ClaimItem]:
        # Index evidence by type for quick lookup
        evidence_by_type: Dict[str, List[EvidenceItem]] = {}
        for ev in evidence:
            evidence_by_type.setdefault(ev.evidence_type, []).append(ev)

        updated_claims: List[ClaimItem] = []

        for claim in claims:
            c = claim.model_copy()
            category = (c.claim_category or "").lower()

            # Rule 1: Organisation Claims
            if category == "organisation":
                related_ev = (
                    evidence_by_type.get("domain_registration", [])
                    + evidence_by_type.get("organisation_consistency", [])
                    + evidence_by_type.get("dns_records", [])
                )
                c.evidence_ids = [e.evidence_id for e in related_ev if e.status == "available"]

                # If domain registration or DNS was found, technical signals are active but cannot prove legitimacy
                has_active_domain = any(
                    e.status == "available" for e in evidence_by_type.get("domain_registration", [])
                )
                if has_active_domain or context.primary_domain:
                    c.verification_status = "inconclusive"
                    c.verification_explanation = (
                        f"Technical records exist for domain '{context.primary_domain or 'unknown'}'. "
                        "However, domain existence alone does not confirm that the claimed organisation exists or that this opportunity was authorized. "
                        "Authoritative corporate registries are not verified."
                    )
                else:
                    c.verification_status = "not_checked"
                    c.verification_explanation = (
                        "No technical domain was available to cross-reference against the claimed organisation. "
                        "Retained as not_checked."
                    )

            # Rule 2: Recruiter Claims
            elif category == "recruiter":
                related_ev = evidence_by_type.get("email_domain_consistency", [])
                c.evidence_ids = [e.evidence_id for e in related_ev if e.status == "available"]

                # Check observations
                email_obs = [o for o in observations if o.category == "email"]
                if any(o.finding == "free_email_provider" for o in email_obs):
                    c.verification_status = "inconclusive"
                    c.verification_explanation = (
                        "Recruiter contact utilizes a free public webmail address rather than a verified enterprise domain. "
                        "This observation indicates informal communication, but cannot confirm or refute recruiter identity on technical evidence alone."
                    )
                elif any(o.finding == "different_domain" for o in email_obs):
                    c.verification_status = "inconclusive"
                    c.verification_explanation = (
                        "Recruiter email domain differs from the opportunity website domain. "
                        "This divergence was noted, but does not definitively establish impersonation."
                    )
                elif any(o.finding == "matching_domain" for o in email_obs):
                    c.verification_status = "inconclusive"
                    c.verification_explanation = (
                        "Recruiter email domain corresponds to the opportunity website domain. "
                        "While technically consistent, unauthenticated message text cannot guarantee sender identity without cryptographic email headers."
                    )
                else:
                    c.verification_status = "not_checked"
                    c.verification_explanation = (
                        "Technical evidence cannot independently establish recruiter identity or employment authority."
                    )

            # Rule 3: Application & URL Claims
            elif category == "application":
                related_ev = (
                    evidence_by_type.get("url_consistency", [])
                    + evidence_by_type.get("domain_registration", [])
                    + evidence_by_type.get("dns_records", [])
                )
                c.evidence_ids = [e.evidence_id for e in related_ev if e.status == "available"]

                url_obs = [o for o in observations if o.category == "url"]
                if any(o.finding == "raw_ip_host" for o in url_obs):
                    c.verification_status = "inconclusive"
                    c.verification_explanation = (
                        "Application URL targets a raw IP address instead of a standard corporate domain."
                    )
                elif any(e.status == "available" for e in related_ev):
                    c.verification_status = "inconclusive"
                    c.verification_explanation = (
                        "Application URL structure and DNS routing were evaluated. "
                        "Routing is active, but technical accessibility does not establish that the portal is genuine or safe."
                    )
                else:
                    c.verification_status = "not_checked"
                    c.verification_explanation = "Application URL could not be verified on external technical registries."

            # Rule 4: Suspicious Indicator Claims
            elif category == "suspicious_indicator":
                # Prompt rule: "Do not convert a suspicious indicator into a contradicted factual claim."
                c.verification_status = "inconclusive"
                c.verification_explanation = (
                    "Linguistic red-flag indicator observed in document text. "
                    "Suspicious phrasing is an observational risk factor, not a confirmed factual contradiction."
                )

            # Rule 5: Financial Claims (Salary, Stipend, Fees)
            elif category == "financial":
                # Prompt rule: "Do not claim to verify salary, selection, job availability, scholarship awards, or recruiter identity from DNS or domain-registration information."
                c.verification_status = "not_checked"
                c.evidence_ids = []
                c.verification_explanation = (
                    "Advertised compensation, stipends, and requested fees cannot be verified through DNS, domain registration, or technical network evidence. "
                    "Retained as not_checked pending authoritative registry or employer corroboration."
                )

            # Rule 6: Opportunity / Role Claims
            elif category == "opportunity":
                c.verification_status = "not_checked"
                c.evidence_ids = []
                c.verification_explanation = (
                    "Job openings, internship offerings, and program details cannot be verified through technical network signals. "
                    "Retained as not_checked pending primary corporate careers board verification."
                )

            # Rule 7: Deadline Claims
            elif category == "deadline":
                c.verification_status = "not_checked"
                c.evidence_ids = []
                c.verification_explanation = (
                    "Application deadlines cannot be confirmed through DNS or domain registration records. "
                    "Retained as not_checked."
                )

            # Default fallback for other claims
            else:
                c.verification_status = "not_checked"
                c.verification_explanation = (
                    "This claim is outside the scope of available technical domain and DNS evidence checks. "
                    "Retained as not_checked."
                )

            updated_claims.append(c)

        return updated_claims


verification_service = VerificationService()
