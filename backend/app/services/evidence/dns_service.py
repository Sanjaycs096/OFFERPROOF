import logging
import asyncio
from typing import List, Tuple, Optional, Dict, Any
import httpx

from app.schemas.evidence import EvidenceItem, TechnicalObservation
from app.services.evidence.base import (
    BaseEvidenceProvider,
    VerificationContext,
    is_safe_public_hostname,
)

logger = logging.getLogger(__name__)

# Cloudflare DNS-over-HTTPS (DoH) JSON endpoint
DOH_ENDPOINT = "https://cloudflare-dns.com/dns-query"
DNS_TIMEOUT = 4.0  # seconds

# Record types: 1: A, 28: AAAA, 15: MX, 2: NS, 16: TXT
RECORD_TYPES = {
    "A": 1,
    "AAAA": 28,
    "MX": 15,
    "NS": 2,
    "TXT": 16,
}


class DNSIntelligenceProvider(BaseEvidenceProvider):
    """
    Queries public DNS records via trusted DNS-over-HTTPS (DoH).
    Safely resolves A, AAAA, MX, NS, and TXT records without UDP socket blocks or SSRF risks.
    """

    @property
    def provider_name(self) -> str:
        return "dns_intelligence"

    async def collect(
        self, context: VerificationContext
    ) -> Tuple[List[EvidenceItem], List[TechnicalObservation]]:
        evidence_list: List[EvidenceItem] = []
        observations: List[TechnicalObservation] = []

        target = context.primary_hostname or context.primary_domain
        if not target:
            evidence_list.append(
                EvidenceItem(
                    evidence_id=context.next_evidence_id(),
                    evidence_type="dns_records",
                    source_name="DNS-over-HTTPS",
                    source_url=None,
                    observed_value="No hostname provided for DNS resolution",
                    interpretation="No opportunity website or URL hostname was provided to check DNS records.",
                    status="not_applicable",
                    limitations=[
                        "DNS resolution requires a valid target hostname or domain."
                    ],
                )
            )
            return evidence_list, observations

        if not is_safe_public_hostname(target):
            evidence_list.append(
                EvidenceItem(
                    evidence_id=context.next_evidence_id(),
                    evidence_type="dns_records",
                    source_name="DNS-over-HTTPS",
                    source_url=None,
                    observed_value=f"Target '{target}' is not an authorized public domain",
                    interpretation="Target refers to a private, internal, or non-routable address. External DNS query was skipped.",
                    status="error",
                    limitations=[
                        "Non-routable and private network addresses cannot be queried on public DNS resolvers."
                    ],
                )
            )
            return evidence_list, observations

        # Query record types concurrently
        dns_results: Dict[str, List[str]] = {}
        query_tasks = [
            self._query_doh_record(target, rtype, type_code)
            for rtype, type_code in RECORD_TYPES.items()
        ]

        raw_responses = await asyncio.gather(*query_tasks, return_exceptions=True)

        for (rtype, _), res in zip(RECORD_TYPES.items(), raw_responses):
            if isinstance(res, list):
                dns_results[rtype] = res
            else:
                dns_results[rtype] = []

        # Analyze findings
        has_a = len(dns_results.get("A", [])) > 0
        has_mx = len(dns_results.get("MX", [])) > 0
        has_ns = len(dns_results.get("NS", [])) > 0
        txt_records = dns_results.get("TXT", [])

        # Check for SPF in TXT
        spf_records = [txt for txt in txt_records if "v=spf1" in txt.lower()]

        # Determine overall DNS resolution status
        if has_a or has_ns:
            status_code = "available"
            summary_parts = []
            if has_a:
                summary_parts.append(f"A: {len(dns_results['A'])} records ({dns_results['A'][0]})")
            if has_mx:
                summary_parts.append(f"MX: {len(dns_results['MX'])} servers")
            if has_ns:
                summary_parts.append(f"NS: {len(dns_results['NS'])} nameservers")

            observed_summary = "; ".join(summary_parts) or "DNS records resolved"

            # Plain-language explanation
            interpretation = (
                f"Hostname '{target}' resolves actively on public DNS. "
            )
            if has_mx:
                interpretation += f"Configured with {len(dns_results['MX'])} mail exchanger(s), capable of receiving email. "
            else:
                interpretation += "No MX (mail exchanger) records were returned for this specific hostname. "

            if spf_records:
                interpretation += "Sender Policy Framework (SPF) records are published in TXT. "

            interpretation += "DNS configuration demonstrates active network routing, but does not verify organisational identity or job authenticity."

            observations.append(
                TechnicalObservation(
                    observation_id=context.next_observation_id(),
                    category="dns",
                    label="DNS information available",
                    finding="dns_active",
                    detail=f"Target '{target}' has active DNS records ({', '.join(k for k, v in dns_results.items() if v)}).",
                    severity="neutral",
                )
            )

            if has_mx:
                observations.append(
                    TechnicalObservation(
                        observation_id=context.next_observation_id(),
                        category="dns",
                        label="Mail exchange records present",
                        finding="has_mx",
                        detail=f"Domain has mail exchangers configured: {', '.join(dns_results['MX'][:2])}.",
                        severity="neutral",
                    )
                )
            else:
                observations.append(
                    TechnicalObservation(
                        observation_id=context.next_observation_id(),
                        category="dns",
                        label="Missing mail exchanger (MX) records",
                        finding="no_mx",
                        detail=f"No MX records returned for '{target}'. Note: If an opportunity email uses a separate domain, this is normal.",
                        severity="informational",
                    )
                )
        else:
            status_code = "not_available"
            observed_summary = f"No A or NS records resolved for '{target}'"
            interpretation = (
                f"DNS queries for '{target}' returned no routing addresses. "
                "The domain may be inactive, misspelled, or relying on dynamic DNS."
            )
            observations.append(
                TechnicalObservation(
                    observation_id=context.next_observation_id(),
                    category="dns",
                    label="DNS information unavailable",
                    finding="dns_inactive",
                    detail=f"No public DNS records could be resolved for target '{target}'.",
                    severity="notable",
                )
            )

        evidence_list.append(
            EvidenceItem(
                evidence_id=context.next_evidence_id(),
                evidence_type="dns_records",
                source_name="DNS-over-HTTPS (Cloudflare DoH)",
                source_url=f"{DOH_ENDPOINT}?name={target}",
                observed_value=observed_summary,
                interpretation=interpretation,
                status=status_code,
                limitations=[
                    "DNS records only demonstrate internet routing configuration; they do not establish organisational legitimacy.",
                    "Missing MX records do not automatically indicate fraud (e.g. static landing pages or separate mail subdomains)."
                ],
                raw_data={"target": target, "records": dns_results},
            )
        )

        return evidence_list, observations

    async def _query_doh_record(self, hostname: str, rtype: str, type_code: int) -> List[str]:
        """Queries Cloudflare DoH for a single record type."""
        url = f"{DOH_ENDPOINT}?name={hostname}&type={type_code}"
        try:
            async with httpx.AsyncClient(timeout=DNS_TIMEOUT) as client:
                res = await client.get(url, headers={"Accept": "application/dns-json"})
                if res.status_code != 200:
                    return []
                data = res.json()
                answers = data.get("Answer", [])
                results = []
                for ans in answers:
                    if ans.get("type") == type_code and "data" in ans:
                        results.append(str(ans["data"]).strip('"'))
                return results
        except Exception as e:
            logger.info(f"DoH query for '{hostname}' type {rtype} failed: {type(e).__name__}")
            return []
