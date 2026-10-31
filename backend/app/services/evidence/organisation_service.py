import re
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional, Dict, Any

from app.schemas.evidence import EvidenceItem, TechnicalObservation
from app.services.evidence.base import (
    BaseEvidenceProvider,
    VerificationContext,
    extract_registrable_domain,
)


class BaseOrganisationRegistryAdapter(ABC):
    """
    Adapter interface for authoritative public company registries
    (e.g., SEC EDGAR, UK Companies House, OpenCorporates, India MCA).
    """

    @abstractmethod
    async def query_registry(self, organisation_name: str) -> Dict[str, Any]:
        """Query official government / public registry."""
        pass


class FutureOrganisationRegistryAdapter(BaseOrganisationRegistryAdapter):
    """
    Placeholder adapter for future registry integrations.
    Returns explicit not_available status without fabricating fake registry records.
    """

    async def query_registry(self, organisation_name: str) -> Dict[str, Any]:
        return {
            "status": "not_available",
            "message": "Authoritative corporate registry integration is scheduled for future implementation.",
        }


class OrganisationIdentityConsistencyProvider(BaseEvidenceProvider):
    """
    Cross-references stated organisation names with domain names, email identifiers,
    and reports alignment observations without fabricating corporate registrations.
    """

    def __init__(self, registry_adapter: Optional[BaseOrganisationRegistryAdapter] = None):
        self.registry_adapter = registry_adapter or FutureOrganisationRegistryAdapter()

    @property
    def provider_name(self) -> str:
        return "organisation_identity_consistency"

    async def collect(
        self, context: VerificationContext
    ) -> Tuple[List[EvidenceItem], List[TechnicalObservation]]:
        evidence_list: List[EvidenceItem] = []
        observations: List[TechnicalObservation] = []

        org_name = context.info.organisation.name
        primary_domain = context.primary_domain

        if not org_name:
            evidence_list.append(
                EvidenceItem(
                    evidence_id=context.next_evidence_id(),
                    evidence_type="organisation_consistency",
                    source_name="Organisation Identity Consistency",
                    source_url=None,
                    observed_value="No organization name identified in opportunity claims",
                    interpretation="No organization name was extracted to compare with technical records.",
                    status="not_applicable",
                    limitations=[
                        "Organisation identity analysis requires an identified organisation name."
                    ],
                )
            )
            return evidence_list, observations

        # 1. Compare organisation name with primary domain tokens
        simplified_org = re.sub(r"[^a-z0-9]", "", org_name.lower())
        domain_token = ""
        if primary_domain:
            domain_token = primary_domain.split(".")[0].lower()

        # Check keyword containment
        is_token_in_org = bool(domain_token and (domain_token in simplified_org or simplified_org in domain_token))
        
        # Check against common generic corporate suffixes
        generic_suffixes = {"technologies", "tech", "llc", "inc", "corp", "corporation", "ltd", "limited", "solutions", "systems", "labs", "group"}
        org_words = set(re.findall(r"\b[a-zA-Z]{3,}\b", org_name.lower())) - generic_suffixes
        has_distinctive_match = any(w in domain_token for w in org_words) if domain_token else False

        if primary_domain and (is_token_in_org or has_distinctive_match):
            naming_finding = "name_domain_aligned"
            interpretation = (
                f"Claimed organisation '{org_name}' shows naming token alignment with domain '{primary_domain}'. "
                "This indicates naming consistency between the text and technical link, but does not prove the organisation authorized this specific posting."
            )
            severity = "neutral"
            observations.append(
                TechnicalObservation(
                    observation_id=context.next_observation_id(),
                    category="organisation",
                    label="Organisation name aligns with domain",
                    finding=naming_finding,
                    detail=f"Organisation '{org_name}' has token overlap with domain '{primary_domain}'.",
                    severity="neutral",
                )
            )
        elif primary_domain:
            naming_finding = "name_domain_divergent"
            interpretation = (
                f"Claimed organisation '{org_name}' does not share obvious naming tokens with the submitted domain '{primary_domain}'. "
                "This observation requires candidate due diligence. Organizations frequently use acquired brand names or holding company domains, but divergence warrants verification."
            )
            severity = "informational"
            observations.append(
                TechnicalObservation(
                    observation_id=context.next_observation_id(),
                    category="organisation",
                    label="Organisation name differs from domain",
                    finding=naming_finding,
                    detail=f"No clear naming correspondence between organisation '{org_name}' and domain '{primary_domain}'.",
                    severity="informational",
                )
            )
        else:
            naming_finding = "no_domain_available"
            interpretation = f"Organisation '{org_name}' was stated, but no website or application domain was available for comparison."
            severity = "informational"

        evidence_list.append(
            EvidenceItem(
                evidence_id=context.next_evidence_id(),
                evidence_type="organisation_consistency",
                source_name="Organisation Identity Consistency",
                source_url=None,
                observed_value=f"Organisation: '{org_name}' vs Domain: '{primary_domain or 'None'}' [{naming_finding}]",
                interpretation=interpretation,
                status="available",
                limitations=[
                    "Naming similarity does not establish that the sender actually represents the organisation.",
                    "Authoritative government corporate registry records were NOT consulted; no formal incorporation is established."
                ],
                raw_data={
                    "organisation_name": org_name,
                    "primary_domain": primary_domain,
                    "naming_finding": naming_finding,
                },
            )
        )

        # 2. Authoritative Corporate Registry Check (explicitly not_available adapter)
        registry_res = await self.registry_adapter.query_registry(org_name)
        evidence_list.append(
            EvidenceItem(
                evidence_id=context.next_evidence_id(),
                evidence_type="corporate_registry",
                source_name="Authoritative Corporate Registry Adapter",
                source_url=None,
                observed_value=f"Official corporate registry check for '{org_name}': not_available",
                interpretation=(
                    "Authoritative government corporate registry integration (e.g. SEC EDGAR, Companies House) is not connected in Phase 3. "
                    "OFFERPROOF strictly avoids simulating or inventing corporate incorporation records."
                ),
                status="not_available",
                limitations=[
                    "Official corporate registration status could not be independently queried.",
                    "Absence of a registry check does not imply that the company does not exist."
                ],
                raw_data=registry_res,
            )
        )

        return evidence_list, observations

