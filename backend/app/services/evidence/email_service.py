import os
import re
from typing import List, Tuple, Optional, Set
from app.schemas.evidence import EvidenceItem, TechnicalObservation
from app.services.evidence.base import (
    BaseEvidenceProvider,
    VerificationContext,
    extract_registrable_domain,
    normalize_hostname,
)

# Configurable list of common consumer free email providers
DEFAULT_FREE_EMAIL_PROVIDERS = {
    "gmail.com", "googlemail.com",
    "yahoo.com", "ymail.com", "rocketmail.com",
    "hotmail.com", "outlook.com", "live.com", "msn.com",
    "aol.com", "aim.com",
    "protonmail.com", "proton.me", "pm.me",
    "mail.com", "email.com",
    "zoho.com", "zohomail.com",
    "yandex.com", "yandex.ru",
    "icloud.com", "me.com", "mac.com",
    "gmx.com", "gmx.net",
    "tutanota.com", "tuta.io",
    "fastmail.com",
}


class EmailDomainConsistencyProvider(BaseEvidenceProvider):
    """
    Analyzes recruiter email domain alignment against opportunity domains.
    Identifies free webmail providers and domain matching without concluding fraud.
    """

    def __init__(self, custom_free_providers: Optional[Set[str]] = None):
        self.free_providers = custom_free_providers or DEFAULT_FREE_EMAIL_PROVIDERS

    @property
    def provider_name(self) -> str:
        return "email_domain_consistency"

    async def collect(
        self, context: VerificationContext
    ) -> Tuple[List[EvidenceItem], List[TechnicalObservation]]:
        evidence_list: List[EvidenceItem] = []
        observations: List[TechnicalObservation] = []

        recruiter_email = context.info.recruiter.email
        if not recruiter_email or "@" not in recruiter_email:
            evidence_list.append(
                EvidenceItem(
                    evidence_id=context.next_evidence_id(),
                    evidence_type="email_domain_consistency",
                    source_name="Email Domain Analysis",
                    source_url=None,
                    observed_value="No recruiter email address provided in opportunity text",
                    interpretation="Opportunity does not supply an email contact address for evaluation.",
                    status="not_applicable",
                    limitations=[
                        "Recruiter email consistency can only be evaluated when an explicit email address is present."
                    ],
                )
            )
            return evidence_list, observations

        # Extract domain part
        raw_email_domain = recruiter_email.split("@")[-1].strip().lower()
        email_reg_domain = extract_registrable_domain(raw_email_domain)
        opp_reg_domain = context.primary_domain

        is_free_mail = email_reg_domain in self.free_providers or raw_email_domain in self.free_providers

        # Compare findings
        finding = "not_comparable"
        interpretation = ""
        observed_summary = f"Recruiter email: {recruiter_email} (domain: {raw_email_domain})"
        severity = "informational"
        status = "available"

        if is_free_mail:
            finding = "free_email_provider"
            observed_summary += " [Public Consumer Webmail]"
            interpretation = (
                f"Recruiter email '{recruiter_email}' uses a public consumer webmail provider ({raw_email_domain}). "
                "While small businesses and independent recruiters occasionally use consumer email, formal corporate hiring typically utilizes custom domain infrastructure."
            )
            severity = "notable"
            observations.append(
                TechnicalObservation(
                    observation_id=context.next_observation_id(),
                    category="email",
                    label="Free email provider detected",
                    finding="free_email_provider",
                    detail=f"Recruiter uses consumer webmail provider '{raw_email_domain}' rather than an enterprise domain.",
                    severity="notable",
                )
            )
        elif opp_reg_domain:
            if email_reg_domain == opp_reg_domain:
                finding = "matching_domain"
                observed_summary += f" [Matches Opportunity Domain '{opp_reg_domain}']"
                interpretation = (
                    f"Recruiter email domain '{raw_email_domain}' matches the claimed opportunity website domain '{opp_reg_domain}'. "
                    "This demonstrates technical naming consistency, though email headers must still be verified for sender authentication."
                )
                severity = "neutral"
                observations.append(
                    TechnicalObservation(
                        observation_id=context.next_observation_id(),
                        category="email",
                        label="Email domain matches opportunity domain",
                        finding="matching_domain",
                        detail=f"Recruiter email domain '{raw_email_domain}' corresponds to opportunity domain '{opp_reg_domain}'.",
                        severity="neutral",
                    )
                )
            else:
                finding = "different_domain"
                observed_summary += f" [Differs from Opportunity Domain '{opp_reg_domain}']"
                interpretation = (
                    f"Recruiter email domain '{raw_email_domain}' differs from the opportunity website domain '{opp_reg_domain}'. "
                    "This is a notable observation. Organisations may legitimately use third-party staffing agencies, but domain divergence warrants caution."
                )
                severity = "notable"
                observations.append(
                    TechnicalObservation(
                        observation_id=context.next_observation_id(),
                        category="email",
                        label="Email-domain mismatch",
                        finding="different_domain",
                        detail=f"Recruiter domain '{raw_email_domain}' does not match opportunity domain '{opp_reg_domain}'.",
                        severity="notable",
                    )
                )
        else:
            finding = "not_comparable"
            interpretation = (
                f"Recruiter email domain is '{raw_email_domain}'. No opportunity website or portal domain was provided to compare against."
            )
            severity = "informational"

        evidence_list.append(
            EvidenceItem(
                evidence_id=context.next_evidence_id(),
                evidence_type="email_domain_consistency",
                source_name="Email Domain Analysis",
                source_url=None,
                observed_value=observed_summary,
                interpretation=interpretation,
                status=status,
                limitations=[
                    "A different email domain is an observation, not proof of impersonation. Organisations may use outsourced recruitment agencies.",
                    "Matching email domains can be spoofed in unauthenticated message headers without SPF/DKIM checks."
                ],
                raw_data={
                    "recruiter_email": recruiter_email,
                    "email_domain": raw_email_domain,
                    "is_free_provider": is_free_mail,
                    "comparison_finding": finding,
                    "compared_against": opp_reg_domain,
                },
            )
        )

        return evidence_list, observations
