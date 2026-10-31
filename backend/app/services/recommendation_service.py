import logging
from typing import List, Optional
from app.schemas.assessment import (
    AssessmentLevel,
    AssessmentFinding,
    SafetyRecommendation,
    UnverifiedClaim,
    NextStepItem,
)
from app.schemas.extraction import ExtractedInformation

logger = logging.getLogger(__name__)


class RecommendationService:
    """
    Generates contextual safety recommendations and a prioritized action checklist
    based on observed assessment findings, unverified claims, and guidance levels.
    """

    def generate_recommendations(
        self,
        assessment_level: AssessmentLevel,
        findings: List[AssessmentFinding],
        unverified_claims: List[UnverifiedClaim],
        extracted_info: Optional[ExtractedInformation] = None,
    ) -> List[SafetyRecommendation]:
        recommendations: List[SafetyRecommendation] = []
        rec_counter = 1

        finding_titles = [f.title.lower() for f in findings]
        finding_severities = [f.severity for f in findings]
        has_fee = any("fee" in t or "payment" in t for t in finding_titles)
        has_email_issue = any("email" in t or "webmail" in t for t in finding_titles)
        has_domain_issue = any("domain" in t or "ip address" in t or "protocol" in t for t in finding_titles)
        has_suspicious_text = any("pressure" in t or "suspicious" in t or "urgency" in t for t in finding_titles)

        # 1. Payment Safety (Triggered when fees or payments are requested)
        if has_fee:
            recommendations.append(
                SafetyRecommendation(
                    recommendation_id=f"REC-{rec_counter:03d}",
                    topic="payment_safety",
                    title="Do not pay any upfront registration, processing, or training fee",
                    advice=(
                        "Legitimate employers, internship hosts, and reputable scholarship providers do not require "
                        "candidates to pay upfront fees to secure a position or undergo onboarding. "
                        "Do not send money, gift cards, or cryptocurrency. Confirm the recruitment policy directly "
                        "on the organization's official careers portal before taking any financial action."
                    ),
                    priority=1,
                )
            )
            rec_counter += 1

        # 2. Personal Information Protection (Triggered on caution, high caution, or fee requests)
        if assessment_level in (AssessmentLevel.HIGH_CAUTION, AssessmentLevel.NEEDS_CAREFUL_REVIEW) or has_fee:
            recommendations.append(
                SafetyRecommendation(
                    recommendation_id=f"REC-{rec_counter:03d}",
                    topic="personal_info",
                    title="Protect sensitive personal, financial, and identity records",
                    advice=(
                        "Never disclose bank account details, credit card numbers, OTPs, account passwords, "
                        "or national identity documents (such as passport copies or national ID numbers) "
                        "during initial outreach. Genuine recruitment evaluations do not require sensitive "
                        "banking or identity credentials prior to formal in-person or verified virtual interviews."
                    ),
                    priority=1,
                )
            )
            rec_counter += 1

        # 3. Recruiter Identity Verification (Triggered when email issues or divergence observed)
        if has_email_issue:
            recommendations.append(
                SafetyRecommendation(
                    recommendation_id=f"REC-{rec_counter:03d}",
                    topic="recruiter_identity",
                    title="Independently verify the recruiter's identity and organizational authority",
                    advice=(
                        "Do not rely solely on the contact details provided in the message. "
                        "Search for the company's verified website or telephone switchboard, contact their HR "
                        "department through independently verified channels, and ask to confirm that this individual "
                        "is authorized to recruit on their behalf."
                    ),
                    priority=2,
                )
            )
            rec_counter += 1

        # 4. Domain & Portal Verification (Triggered when domain anomalies or new registrations observed)
        if has_domain_issue:
            recommendations.append(
                SafetyRecommendation(
                    recommendation_id=f"REC-{rec_counter:03d}",
                    topic="domain_safety",
                    title="Independently locate and verify the official company website",
                    advice=(
                        "Rather than clicking links inside unsolicited messages, open an independent browser window "
                        "and search for the company through verified corporate registries or reputable search engines. "
                        "Check whether the opportunity is posted on the company's official /careers page."
                    ),
                    priority=2,
                )
            )
            rec_counter += 1

        # 5. Opportunity Details & Unverified Claims (Triggered when salary/stipend/guarantee claims exist)
        if unverified_claims:
            recommendations.append(
                SafetyRecommendation(
                    recommendation_id=f"REC-{rec_counter:03d}",
                    topic="unverified_details",
                    title="Independently confirm compensation, selection terms, and deadlines",
                    advice=(
                        "Advertised compensation (stipends or salaries), selection guarantees, and application "
                        "deadlines cannot be verified through technical network intelligence. Always request an official, "
                        "written offer letter with full job specifications and verify it with the employer before making commitments."
                    ),
                    priority=3,
                )
            )
            rec_counter += 1

        # 6. Insufficient Evidence Scenario
        if assessment_level == AssessmentLevel.INSUFFICIENT_EVIDENCE:
            recommendations.append(
                SafetyRecommendation(
                    recommendation_id=f"REC-{rec_counter:03d}",
                    topic="recruiter_identity",
                    title="Request complete organizational and contact details from the sender",
                    advice=(
                        "The submitted announcement lacks basic technical indicators (such as a website or official email domain). "
                        "Request full corporate registration details, an official corporate website, and a verifiable corporate email "
                        "before engaging further."
                    ),
                    priority=1,
                )
            )
            rec_counter += 1

        # 7. Baseline good practice if limited concerns detected
        if assessment_level == AssessmentLevel.LIMITED_CONCERNS_DETECTED and not recommendations:
            recommendations.append(
                SafetyRecommendation(
                    recommendation_id=f"REC-{rec_counter:03d}",
                    topic="unverified_details",
                    title="Verify the opening on the employer's official careers portal",
                    advice=(
                        "Although technical indicators were consistent with standard operations, technical domain "
                        "checks cannot guarantee that an opportunity is legitimate or authorized. Verify the opening "
                        "directly on the employer's official careers page."
                    ),
                    priority=2,
                )
            )

        # Sort recommendations by priority (1 first, then 2, then 3)
        recommendations.sort(key=lambda r: r.priority)
        return recommendations

    def generate_next_steps(
        self,
        assessment_level: AssessmentLevel,
        findings: List[AssessmentFinding],
        unverified_claims: List[UnverifiedClaim],
    ) -> List[NextStepItem]:
        finding_titles = [f.title.lower() for f in findings]
        has_fee = any("fee" in t or "payment" in t for t in finding_titles)
        has_email = any("email" in t or "webmail" in t for t in finding_titles)
        steps: List[NextStepItem] = []

        step_num = 1
        if has_fee:
            steps.append(
                NextStepItem(
                    step_number=step_num,
                    action="Pause all payment workflows immediately and do not transfer funds.",
                    rationale="Legitimate employers do not require candidates to pay application or equipment fees upfront.",
                )
            )
            step_num += 1

        if assessment_level == AssessmentLevel.INSUFFICIENT_EVIDENCE:
            steps.append(
                NextStepItem(
                    step_number=step_num,
                    action="Ask the recruiter to provide their official company website and corporate email domain.",
                    rationale="Independent technical checks cannot evaluate an opportunity without verifiable domains or email identifiers.",
                )
            )
            step_num += 1
        else:
            steps.append(
                NextStepItem(
                    step_number=step_num,
                    action="Navigate independently to the organization's official website via a search engine.",
                    rationale="Ensures you are evaluating the authentic corporate portal rather than an unverified lookalike link.",
                )
            )
            step_num += 1

        steps.append(
            NextStepItem(
                step_number=step_num,
                action="Confirm the vacancy on the official company careers board or via their HR department.",
                rationale="Validates that the position exists and has been authorized by the organization.",
            )
        )
        step_num += 1

        if has_email:
            steps.append(
                NextStepItem(
                    step_number=step_num,
                    action="Cross-check the recruiter's name and position using professional directories or LinkedIn.",
                    rationale="Helps verify whether the individual is actively employed by the claimed organization.",
                )
            )
            step_num += 1

        steps.append(
            NextStepItem(
                step_number=step_num,
                action="Never disclose banking details, PINs, OTPs, or government IDs before formal verified onboarding.",
                rationale="Protects against identity theft and unauthorized financial transactions during recruitment.",
            )
        )

        return steps


recommendation_service = RecommendationService()
