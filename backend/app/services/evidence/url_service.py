import ipaddress
from typing import List, Tuple, Optional
from urllib.parse import urlparse

from app.schemas.evidence import EvidenceItem, TechnicalObservation
from app.services.evidence.base import (
    BaseEvidenceProvider,
    VerificationContext,
    extract_registrable_domain,
    normalize_hostname,
    is_safe_public_hostname,
)


class URLConsistencyProvider(BaseEvidenceProvider):
    """
    Performs structural, protocol, and hostname consistency analysis on submitted URLs.
    Does NOT issue outbound HTTP GET requests or scrape target sites.
    """

    @property
    def provider_name(self) -> str:
        return "url_consistency"

    async def collect(
        self, context: VerificationContext
    ) -> Tuple[List[EvidenceItem], List[TechnicalObservation]]:
        evidence_list: List[EvidenceItem] = []
        observations: List[TechnicalObservation] = []

        raw_url = context.application_url or context.info.application.application_url or context.info.organisation.website
        if not raw_url or not raw_url.strip():
            evidence_list.append(
                EvidenceItem(
                    evidence_id=context.next_evidence_id(),
                    evidence_type="url_consistency",
                    source_name="Structural URL Inspection",
                    source_url=None,
                    observed_value="No application URL or website link submitted",
                    interpretation="No URL was provided for protocol and hostname structural auditing.",
                    status="not_applicable",
                    limitations=[
                        "URL inspection requires an explicit web address."
                    ],
                )
            )
            return evidence_list, observations

        cleaned_url = raw_url.strip()
        has_scheme = "://" in cleaned_url
        effective_url = cleaned_url if has_scheme else "https://" + cleaned_url

        try:
            parsed = urlparse(effective_url)
            scheme = (parsed.scheme or "unknown").lower()
            hostname = (parsed.hostname or "").lower()
        except Exception:
            evidence_list.append(
                EvidenceItem(
                    evidence_id=context.next_evidence_id(),
                    evidence_type="url_consistency",
                    source_name="Structural URL Inspection",
                    source_url=None,
                    observed_value=f"Malformed URL string: '{cleaned_url}'",
                    interpretation="URL could not be parsed into valid components.",
                    status="error",
                    limitations=["Malformed URL strings cannot be structurally validated."],
                )
            )
            return evidence_list, observations

        # 1. Protocol check
        is_https = scheme == "https"
        protocol_finding = "https" if is_https else "http_only"
        protocol_detail = (
            "URL utilizes HTTPS (encrypted transport)."
            if is_https
            else f"URL uses unencrypted '{scheme}' protocol without transport security."
        )

        observations.append(
            TechnicalObservation(
                observation_id=context.next_observation_id(),
                category="url",
                label="Transport protocol",
                finding=protocol_finding,
                detail=protocol_detail,
                severity="neutral" if is_https else "notable",
            )
        )

        # 2. Check if hostname is an IP address
        is_ip = False
        try:
            ipaddress.ip_address(hostname)
            is_ip = True
            observations.append(
                TechnicalObservation(
                    observation_id=context.next_observation_id(),
                    category="url",
                    label="IP address in URL",
                    finding="raw_ip_host",
                    detail=f"URL specifies a raw IP address ({hostname}) instead of a named domain.",
                    severity="notable",
                )
            )
        except ValueError:
            pass

        # 3. Domain alignment check
        app_domain = extract_registrable_domain(context.app_hostname)
        web_domain = extract_registrable_domain(context.website_hostname)

        domain_relation_finding = "single_domain"
        relation_detail = "Single domain supplied across application and website fields."

        if app_domain and web_domain:
            if app_domain == web_domain:
                if context.app_hostname != context.website_hostname:
                    domain_relation_finding = "subdomain_match"
                    relation_detail = (
                        f"Application hostname '{context.app_hostname}' is a verified subdomain "
                        f"of the primary organization domain '{web_domain}'."
                    )
                else:
                    domain_relation_finding = "identical_domain"
                    relation_detail = f"Application URL directly targets the primary domain '{web_domain}'."
            else:
                domain_relation_finding = "domain_divergence"
                relation_detail = (
                    f"Application portal domain '{app_domain}' differs from the claimed corporate website '{web_domain}'. "
                    "Legitimate organizations often host hiring on third-party applicant tracking systems (e.g. greenhouse.io, lever.co, workday), but unknown destinations require due diligence."
                )
                observations.append(
                    TechnicalObservation(
                        observation_id=context.next_observation_id(),
                        category="url",
                        label="Application vs website domain divergence",
                        finding="domain_divergence",
                        detail=relation_detail,
                        severity="informational",
                    )
                )

        observed_text = f"URL: {cleaned_url} [Scheme: {scheme.upper()}, Host: {hostname}]"
        interpretation_text = (
            f"Structural analysis completed for '{hostname}'. Protocol: {scheme.upper()}. "
            f"{relation_detail} "
            "HTTPS confirms transport encryption between browser and server, but does NOT establish that the server owner is honest or genuine."
        )

        evidence_list.append(
            EvidenceItem(
                evidence_id=context.next_evidence_id(),
                evidence_type="url_consistency",
                source_name="Structural URL Inspection",
                source_url=None,
                observed_value=observed_text,
                interpretation=interpretation_text,
                status="available",
                limitations=[
                    "HTTPS indicates encrypted transport security, NOT organizational legitimacy.",
                    "The destination website was NOT visited or scraped in accordance with Phase 3 SSRF security boundaries."
                ],
                raw_data={
                    "submitted_url": cleaned_url,
                    "scheme": scheme,
                    "hostname": hostname,
                    "is_https": is_https,
                    "is_ip": is_ip,
                    "domain_relation": domain_relation_finding,
                },
            )
        )

        return evidence_list, observations

