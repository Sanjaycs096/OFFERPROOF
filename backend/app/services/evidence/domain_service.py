import logging
from datetime import datetime, timezone
from typing import List, Tuple, Optional, Dict, Any
import httpx

from app.schemas.evidence import EvidenceItem, TechnicalObservation
from app.services.evidence.base import (
    BaseEvidenceProvider,
    VerificationContext,
    is_safe_public_hostname,
    extract_registrable_domain,
)

logger = logging.getLogger(__name__)

# Trusted RDAP service bootstrap
RDAP_BASE_URL = "https://rdap.org/domain"
REQUEST_TIMEOUT = 5.0  # seconds


class DomainIntelligenceProvider(BaseEvidenceProvider):
    """
    Retrieves and interprets domain registration metadata via trusted RDAP endpoints.
    Enforces safe public domain validation and strict SSRF boundaries.
    """

    @property
    def provider_name(self) -> str:
        return "domain_intelligence"

    async def collect(
        self, context: VerificationContext
    ) -> Tuple[List[EvidenceItem], List[TechnicalObservation]]:
        evidence_list: List[EvidenceItem] = []
        observations: List[TechnicalObservation] = []

        domain = context.primary_domain
        if not domain:
            evidence_list.append(
                EvidenceItem(
                    evidence_id=context.next_evidence_id(),
                    evidence_type="domain_registration",
                    source_name="RDAP",
                    source_url=None,
                    observed_value="No valid domain available for registration lookup",
                    interpretation="No opportunity website or application URL domain was provided for evaluation.",
                    status="not_applicable",
                    limitations=[
                        "Domain intelligence requires a valid submitted website or application domain."
                    ],
                )
            )
            return evidence_list, observations

        # Security check: validate public hostname
        if not is_safe_public_hostname(domain):
            evidence_list.append(
                EvidenceItem(
                    evidence_id=context.next_evidence_id(),
                    evidence_type="domain_registration",
                    source_name="RDAP",
                    source_url=None,
                    observed_value=f"Domain '{domain}' is not an authorized public domain",
                    interpretation="The domain refers to a private, localhost, or invalid address. External RDAP querying was skipped for security.",
                    status="error",
                    limitations=[
                        "Internal, localhost, and non-routable domains cannot be queried via public RDAP registries."
                    ],
                )
            )
            observations.append(
                TechnicalObservation(
                    observation_id=context.next_observation_id(),
                    category="domain",
                    label="Invalid or private domain",
                    finding="invalid_domain",
                    detail=f"Target domain '{domain}' is non-routable or private.",
                    severity="notable",
                )
            )
            return evidence_list, observations

        # Query RDAP
        rdap_url = f"{RDAP_BASE_URL}/{domain}"
        try:
            async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT, follow_redirects=True) as client:
                res = await client.get(
                    rdap_url,
                    headers={"Accept": "application/rdap+json, application/json"},
                )

                if res.status_code == 200:
                    data = res.json()
                    evidence, obs = self._parse_rdap_success(context, domain, rdap_url, data)
                    evidence_list.append(evidence)
                    if obs:
                        observations.append(obs)
                elif res.status_code == 404:
                    evidence_list.append(
                        EvidenceItem(
                            evidence_id=context.next_evidence_id(),
                            evidence_type="domain_registration",
                            source_name="RDAP",
                            source_url=rdap_url,
                            observed_value=f"Domain '{domain}' was not found in public RDAP registry",
                            interpretation="No active registration record was returned by the authoritative registry. The domain may be unregistered, newly created, or under a non-participating TLD registry.",
                            status="not_available",
                            limitations=[
                                "Some country-code TLD registries (ccTLDs) do not publish complete public RDAP data.",
                                "A 404 response does not prove that a domain does not exist on DNS."
                            ],
                            raw_data={"http_status": 404},
                        )
                    )
                    observations.append(
                        TechnicalObservation(
                            observation_id=context.next_observation_id(),
                            category="domain",
                            label="Domain registration record unavailable",
                            finding="rdap_not_found",
                            detail=f"Public RDAP registry returned no registration entity for '{domain}'.",
                            severity="informational",
                        )
                    )
                else:
                    evidence_list.append(
                        EvidenceItem(
                            evidence_id=context.next_evidence_id(),
                            evidence_type="domain_registration",
                            source_name="RDAP",
                            source_url=rdap_url,
                            observed_value=f"RDAP registry returned HTTP status {res.status_code}",
                            interpretation="The RDAP service was reached but could not provide registration records.",
                            status="error",
                            limitations=[
                                "Registry servers may apply rate limiting or temporary outages."
                            ],
                            raw_data={"http_status": res.status_code},
                        )
                    )
        except Exception as e:
            logger.info(f"RDAP lookup for '{domain}' failed or timed out: {type(e).__name__}")
            evidence_list.append(
                EvidenceItem(
                    evidence_id=context.next_evidence_id(),
                    evidence_type="domain_registration",
                    source_name="RDAP",
                    source_url=rdap_url,
                    observed_value=f"RDAP query failed or timed out: {type(e).__name__}",
                    interpretation="The external registration registry did not respond within the allocated timeout period.",
                    status="not_available",
                    limitations=[
                        "Network connectivity or registry rate limits can prevent real-time RDAP lookups.",
                        "Absence of RDAP data does not establish that a domain is fraudulent."
                    ],
                )
            )

        return evidence_list, observations

    def _parse_rdap_success(
        self,
        context: VerificationContext,
        domain: str,
        rdap_url: str,
        data: Dict[str, Any],
    ) -> Tuple[EvidenceItem, Optional[TechnicalObservation]]:
        events = data.get("events", [])
        reg_date_str = None
        for ev in events:
            if ev.get("eventAction") == "registration":
                reg_date_str = ev.get("eventDate")
                break

        # Extract registrar if available
        entities = data.get("entities", [])
        registrar_name = None
        for ent in entities:
            roles = ent.get("roles", [])
            if "registrar" in roles:
                vcard = ent.get("vcardArray", [])
                if len(vcard) > 1 and isinstance(vcard[1], list):
                    for item in vcard[1]:
                        if len(item) > 3 and item[0] == "fn":
                            registrar_name = item[3]
                            break
                if not registrar_name:
                    registrar_name = ent.get("handle")

        status_list = data.get("status", [])
        status_summary = ", ".join(status_list) if status_list else "active"

        raw_info = {
            "domain": domain,
            "registration_date": reg_date_str,
            "registrar": registrar_name,
            "status": status_list,
        }

        # Calculate age
        age_days = None
        finding_code = "unknown_age"
        age_interpretation = "Registration date was not specified in the RDAP response."
        severity = "informational"

        if reg_date_str:
            try:
                # Parse ISO date string (handle trailing Z or offset)
                clean_date = reg_date_str.replace("Z", "+00:00")
                dt = datetime.fromisoformat(clean_date)
                now = datetime.now(timezone.utc)
                age_days = max(0, (now - dt).days)
                raw_info["age_days"] = age_days

                if age_days < 30:
                    finding_code = "new_domain"
                    age_interpretation = (
                        f"Domain was registered very recently ({age_days} days ago). "
                        "Newly created domains are frequently observed in recruitment scams, but legitimate newly formed entities also create new domains."
                    )
                    severity = "notable"
                elif 30 <= age_days <= 180:
                    finding_code = "recent_domain"
                    age_interpretation = (
                        f"Domain was registered relatively recently ({age_days} days ago). "
                        "This is a notable observation requiring corroboration against the claimed organisation's founding date."
                    )
                    severity = "informational"
                else:
                    finding_code = "established_domain"
                    age_interpretation = (
                        f"Domain has been registered for {age_days} days ({age_days // 365} years). "
                        "The domain is not newly registered, though older domains can still be compromised or repurposed."
                    )
                    severity = "neutral"
            except Exception:
                age_interpretation = f"Registration date '{reg_date_str}' could not be parsed into a numeric age."

        observed_text = f"Registration: {reg_date_str or 'Unavailable'}"
        if age_days is not None:
            observed_text += f" ({age_days} days old)"
        if registrar_name:
            observed_text += f" via {registrar_name}"

        evidence = EvidenceItem(
            evidence_id=context.next_evidence_id(),
            evidence_type="domain_registration",
            source_name="RDAP",
            source_url=rdap_url,
            observed_value=observed_text,
            interpretation=age_interpretation,
            status="available",
            limitations=[
                "Domain registration age does not establish organisational legitimacy.",
                "Established domains can be spoofed or compromised; new domains may represent legitimate startups."
            ],
            raw_data=raw_info,
        )

        observation = TechnicalObservation(
            observation_id=context.next_observation_id(),
            category="domain",
            label="Domain age observation",
            finding=finding_code,
            detail=age_interpretation,
            severity=severity,
        )

        return evidence, observation

