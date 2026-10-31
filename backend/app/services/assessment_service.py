import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

from app.schemas.extraction import ExtractedInformation, ClaimItem, SuspiciousIndicator
from app.schemas.evidence import EvidenceItem, TechnicalObservation
from app.schemas.verification import VerificationSummary, VerificationResponse
from app.schemas.assessment import (
    AssessmentLevel,
    FindingSeverity,
    AssessmentFinding,
    SafetyRecommendation,
    VerifiedFact,
    UnverifiedClaim,
    NextStepItem,
    AssessmentOverview,
    AssessmentReport,
    AssessmentRequest,
    AssessmentResponse,
)
from app.services.recommendation_service import recommendation_service

logger = logging.getLogger(__name__)

OFFERPROOF_ASSESSMENT_LIMITATIONS = [
    "OfferProof assessments evaluate publicly accessible technical signals (DNS, RDAP, email domains, URL protocols). They cannot inspect private employer databases.",
    "Assessment categories are safety guidance levels, not legal determinations or definitive fraud verdicts.",
    "A category of 'Limited concerns detected' indicates that technical checks found few red flags; it must NEVER be interpreted as confirmation that the opportunity is genuine.",
    "Authoritative government corporate registries (e.g. SEC, Companies House, MCA) and university accredited rosters were not queried; incorporation remains unverified.",
    "Financial offers (salaries, stipends, bonuses), hiring guarantees, and application deadlines are unverifiable through public network records.",
    "In accordance with security safeguards, OfferProof never downloads, executes, or crawls user-provided application links."
]


class AssessmentService:
    """
    Deterministic Explainable Assessment Engine for OFFERPROOF.
    Synthesizes extracted claims, technical observations, and independent evidence
    into transparent, evidence-based assessment reports with actionable guidance.
    """

    def generate_assessment(
        self,
        extracted_info: Optional[ExtractedInformation],
        claims: List[ClaimItem],
        evidence: List[EvidenceItem],
        observations: List[TechnicalObservation],
        verification_summary: Optional[VerificationSummary] = None,
        limitations: Optional[List[str]] = None,
        suspicious_indicators: Optional[List[SuspiciousIndicator]] = None,
    ) -> AssessmentReport:
        # 1. Extract verified technical facts
        verified_facts = self._compile_verified_facts(evidence, observations)

        # 2. Extract unverified claims
        unverified_claims = self._compile_unverified_claims(claims)

        # 3. Generate explainable findings
        findings = self._generate_findings(
            extracted_info, claims, evidence, observations, suspicious_indicators
        )

        # 4. Evaluate assessment category based on deterministic rules
        assessment_level, label, summary_text = self._determine_assessment_level(
            extracted_info, claims, evidence, observations, findings
        )

        # 5. Generate contextual safety recommendations
        recommendations = recommendation_service.generate_recommendations(
            assessment_level=assessment_level,
            findings=findings,
            unverified_claims=unverified_claims,
            extracted_info=extracted_info,
        )

        # 6. Generate prioritized next steps
        next_steps = recommendation_service.generate_next_steps(
            assessment_level=assessment_level,
            findings=findings,
            unverified_claims=unverified_claims,
        )

        # 7. Merge limitations
        combined_limitations = list(dict.fromkeys(
            (limitations or []) + OFFERPROOF_ASSESSMENT_LIMITATIONS
        ))

        overview = AssessmentOverview(
            assessment_level=assessment_level,
            assessment_label=label,
            summary=summary_text,
            important_notice=(
                "This is an evidence-based assessment, not a guarantee of legitimacy or fraud. "
                "Never make financial payments or share sensitive documents based on unverified announcements."
            ),
        )

        return AssessmentReport(
            assessment=overview,
            findings=findings,
            recommendations=recommendations,
            verified_facts=verified_facts,
            unverified_claims=unverified_claims,
            limitations=combined_limitations,
            next_steps=next_steps,
        )

    def assess(self, request: AssessmentRequest) -> AssessmentResponse:
        data = request.get_effective_data()
        report = self.generate_assessment(
            extracted_info=data.get("extracted_information"),
            claims=data.get("claims", []),
            evidence=data.get("evidence", []),
            observations=data.get("technical_observations", []),
            verification_summary=data.get("verification_summary"),
            limitations=data.get("limitations"),
        )
        return AssessmentResponse(
            success=True,
            assessment=report.assessment,
            findings=report.findings,
            recommendations=report.recommendations,
            verified_facts=report.verified_facts,
            unverified_claims=report.unverified_claims,
            limitations=report.limitations,
            next_steps=report.next_steps,
            verification_summary=data.get("verification_summary"),
        )

    # -------------------------------------------------------------------------
    # Private Helpers: Verified Facts
    # -------------------------------------------------------------------------
    def _compile_verified_facts(
        self,
        evidence: List[EvidenceItem],
        observations: List[TechnicalObservation],
    ) -> List[VerifiedFact]:
        facts: List[VerifiedFact] = []
        fact_idx = 1

        for ev in evidence:
            if ev.status != "available":
                continue
            ev_data = getattr(ev, "raw_data", None) or getattr(ev, "data", None) or {}
            retrieved_str = (
                ev.retrieved_at.isoformat()
                if hasattr(ev.retrieved_at, "isoformat")
                else str(ev.retrieved_at)
            )

            fact_added = False
            if ev.evidence_type == "domain_registration":
                reg_date = ev_data.get("registration_date")
                age_days = ev_data.get("age_days", ev_data.get("domain_age_days"))
                registrar = ev_data.get("registrar") or "Known Registrar"
                domain = ev_data.get("domain") or "Target domain"

                stmt = f"Domain '{domain}' was registered with {registrar}"
                if reg_date:
                    stmt += f" on {reg_date}"
                if age_days is not None:
                    stmt += f" ({age_days} days ago)"
                stmt += "."

                facts.append(
                    VerifiedFact(
                        fact_id=f"FCT-{fact_idx:03d}",
                        category="domain",
                        statement=stmt,
                        source_name=ev.source_name,
                        retrieved_at=retrieved_str,
                    )
                )
                fact_idx += 1
                fact_added = True

            elif ev.evidence_type == "dns_records":
                domain = ev_data.get("hostname") or ev_data.get("domain") or "Target domain"
                a_recs = ev_data.get("a_records", [])
                mx_recs = ev_data.get("mx_records", [])

                if a_recs:
                    facts.append(
                        VerifiedFact(
                            fact_id=f"FCT-{fact_idx:03d}",
                            category="dns",
                            statement=f"Domain '{domain}' has {len(a_recs)} active IPv4 (A) record(s) resolving to {', '.join(a_recs[:2])}.",
                            source_name=ev.source_name,
                            retrieved_at=retrieved_str,
                        )
                    )
                    fact_idx += 1
                    fact_added = True

                if mx_recs:
                    facts.append(
                        VerifiedFact(
                            fact_id=f"FCT-{fact_idx:03d}",
                            category="dns",
                            statement=f"Domain '{domain}' has {len(mx_recs)} configured mail exchange (MX) server(s).",
                            source_name=ev.source_name,
                            retrieved_at=retrieved_str,
                        )
                    )
                    fact_idx += 1
                    fact_added = True

            elif ev.evidence_type == "email_domain_consistency":
                recruiter_email = ev_data.get("recruiter_email")
                consistency = ev_data.get("consistency_type") or ev_data.get("finding")
                if recruiter_email or consistency:
                    facts.append(
                        VerifiedFact(
                            fact_id=f"FCT-{fact_idx:03d}",
                            category="email",
                            statement=f"Recruiter email '{recruiter_email or 'contact'}' evaluated: consistency is '{consistency or 'evaluated'}'.",
                            source_name=ev.source_name,
                            retrieved_at=retrieved_str,
                        )
                    )
                    fact_idx += 1
                    fact_added = True

            elif ev.evidence_type == "url_consistency":
                scheme = ev_data.get("scheme", "https")
                hostname = ev_data.get("hostname")
                if hostname:
                    facts.append(
                        VerifiedFact(
                            fact_id=f"FCT-{fact_idx:03d}",
                            category="protocol",
                            statement=f"Application URL host '{hostname}' utilizes '{scheme.upper()}' encryption protocol.",
                            source_name=ev.source_name,
                            retrieved_at=retrieved_str,
                        )
                    )
                    fact_idx += 1
                    fact_added = True

            # If not covered by specific branch, create verified fact from observed_value
            if not fact_added and ev.observed_value:
                facts.append(
                    VerifiedFact(
                        fact_id=f"FCT-{fact_idx:03d}",
                        category=ev.evidence_type.split("_")[0],
                        statement=ev.observed_value,
                        source_name=ev.source_name,
                        retrieved_at=retrieved_str,
                    )
                )
                fact_idx += 1

        return facts

    # -------------------------------------------------------------------------
    # Private Helpers: Unverified Claims
    # -------------------------------------------------------------------------
    def _compile_unverified_claims(self, claims: List[ClaimItem]) -> List[UnverifiedClaim]:
        unverified: List[UnverifiedClaim] = []

        for c in claims:
            # All claims tagged not_checked or inconclusive regarding ground truth
            cat = (c.claim_category or "").lower()
            if c.verification_status == "not_checked":
                reason = "Technical DNS and domain records cannot verify internal organization terms or facts."
                if cat == "financial":
                    reason = "Salary figures, stipend amounts, and fee requirements cannot be confirmed through technical network records."
                elif cat == "opportunity":
                    reason = "Job openings, internship curricula, and duties cannot be confirmed via technical network signals."
                elif cat == "deadline":
                    reason = "Application deadlines cannot be checked against technical domain or DNS infrastructure."
                elif cat == "recruiter":
                    reason = "Recruiter employment authorization cannot be verified without authoritative employer HR records."

                unverified.append(
                    UnverifiedClaim(
                        claim_id=c.claim_id,
                        category=c.claim_category,
                        statement=c.claim_text,
                        reason_unverified=reason,
                    )
                )
            elif cat in ("financial", "opportunity", "deadline"):
                # Always treat financial/opportunity/deadline as unverified ground truth even if status is inconclusive
                unverified.append(
                    UnverifiedClaim(
                        claim_id=c.claim_id,
                        category=c.claim_category,
                        statement=c.claim_text,
                        reason_unverified="Unverifiable through public infrastructure records alone.",
                    )
                )

        return unverified

    # -------------------------------------------------------------------------
    # Private Helpers: Findings Generation
    # -------------------------------------------------------------------------
    def _generate_findings(
        self,
        extracted_info: Optional[ExtractedInformation],
        claims: List[ClaimItem],
        evidence: List[EvidenceItem],
        observations: List[TechnicalObservation],
        suspicious_indicators: Optional[List[SuspiciousIndicator]] = None,
    ) -> List[AssessmentFinding]:
        findings: List[AssessmentFinding] = []
        finding_num = 1

        # Helpers to find related IDs
        def get_claims_by_category(cat: str) -> List[str]:
            return [c.claim_id for c in claims if (c.claim_category or "").lower() == cat.lower()]

        def get_evidence_by_type(ev_type: str) -> List[str]:
            return [e.evidence_id for e in evidence if e.evidence_type == ev_type]

        # 1. UPFRONT FEE CHECK (HIGH CAUTION)
        has_fee = False
        fee_details = []
        fin = None
        if extracted_info:
            fin = getattr(extracted_info, "financial_details", None) or getattr(extracted_info, "financial", None)

        if fin:
            if getattr(fin, "registration_fees", None):
                has_fee = True
                fee_details.append(f"Registration fee: {fin.registration_fees}")
            if getattr(fin, "processing_fees", None):
                has_fee = True
                fee_details.append(f"Processing fee: {fin.processing_fees}")
            if getattr(fin, "training_fees", None):
                has_fee = True
                fee_details.append(f"Training fee: {fin.training_fees}")
            other_reqs = getattr(fin, "other_payment_requests", None) or getattr(fin, "other_fees", None)
            if other_reqs:
                has_fee = True
                req_str = ", ".join(other_reqs) if isinstance(other_reqs, list) else str(other_reqs)
                fee_details.append(f"Other payment request: {req_str}")

        fee_claims = [
            c for c in claims
            if (c.claim_category or "").lower() == "financial"
            and any(kw in c.claim_text.lower() for kw in ("fee", "pay", "charge", "deposit", "cost"))
        ]
        if fee_claims:
            has_fee = True

        fee_indicators = []
        indicators_list = suspicious_indicators or getattr(extracted_info, "suspicious_indicators", []) or []
        for ind in indicators_list:
            phrase = getattr(ind, "phrase", None) or getattr(ind, "statement", "")
            cat = getattr(ind, "category", None) or getattr(ind, "indicator_type", "")
            if any(kw in cat.lower() or kw in phrase.lower() for kw in ("fee", "payment", "money")):
                has_fee = True
                fee_indicators.append(phrase)

        if has_fee:
            detail_str = "; ".join(fee_details) if fee_details else "Upfront fee or registration payment demand"
            findings.append(
                AssessmentFinding(
                    finding_id=f"FND-{finding_num:03d}",
                    title="Upfront registration, processing, or training fee requested",
                    severity=FindingSeverity.HIGH_CAUTION,
                    explanation=(
                        f"The announcement explicitly requests an upfront payment before proceeding: {detail_str}. "
                        "Upfront recruitment, training, or processing fees are a significant warning sign. "
                        "Independently confirm the request through the organisation's official channels before paying."
                    ),
                    related_claim_ids=[c.claim_id for c in fee_claims] or get_claims_by_category("financial"),
                    related_evidence_ids=[],
                    why_it_matters=(
                        "Demanding upfront fees is the single most common pattern in recruitment fraud. "
                        "Once money is transferred, candidates rarely receive the promised role or refund."
                    ),
                    limitations=(
                        "The text confirms that a payment is requested, but technical checks cannot ascertain "
                        "the legal identity or motives of the sender. Some academic contests or certification exams charge entry fees."
                    ),
                    recommended_action=(
                        "Do not pay any fee or deposit. Independently contact the organization through their verified "
                        "public careers directory to verify whether any payment request is authentic."
                    ),
                )
            )
            finding_num += 1

        # 2. FREE PUBLIC WEBMAIL RECRUITER (CAUTION)
        free_email_obs = [o for o in observations if o.finding == "free_email_provider"]
        if free_email_obs:
            email_val = (
                (extracted_info.recruiter.email if extracted_info and extracted_info.recruiter else None)
                or getattr(free_email_obs[0], "target", None)
                or "recruiter contact"
            )
            domain_val = email_val.split("@")[-1] if "@" in email_val else "public webmail"
            findings.append(
                AssessmentFinding(
                    finding_id=f"FND-{finding_num:03d}",
                    title=f"Recruiter contact utilizes a free webmail service (@{domain_val})",
                    severity=FindingSeverity.CAUTION,
                    explanation=(
                        f"The recruiter contact ({email_val}) uses a free public email provider (@{domain_val}) "
                        "rather than an authenticated corporate domain corresponding to the claimed organization."
                    ),
                    related_claim_ids=get_claims_by_category("recruiter"),
                    related_evidence_ids=get_evidence_by_type("email_domain_consistency"),
                    why_it_matters=(
                        "Established organizations almost always communicate through company-owned, authenticated "
                        "email domains. Public webmail accounts can be created anonymously by anyone without organizational affiliation."
                    ),
                    limitations=(
                        "Using a free webmail service does not prove fraud. Small startups, independent researchers, "
                        "and volunteer initiatives sometimes use consumer webmail for communication."
                    ),
                    recommended_action=(
                        "Request communication from the recruiter's official company email address, and confirm their "
                        "employment status with the organization's HR department before sharing personal details."
                    ),
                )
            )
            finding_num += 1

        # 3. RECRUITER EMAIL DOMAIN DIVERGENCE (CAUTION)
        email_diff_obs = [o for o in observations if o.finding == "different_domain"]
        if email_diff_obs:
            email_val = (
                (extracted_info.recruiter.email if extracted_info and extracted_info.recruiter else None)
                or "recruiter"
            )
            email_domain = email_val.split("@")[-1] if "@" in email_val else "recruiter domain"
            org_domain = (
                (extracted_info.organisation.website if extracted_info and extracted_info.organisation else None)
                or "organization domain"
            )
            findings.append(
                AssessmentFinding(
                    finding_id=f"FND-{finding_num:03d}",
                    title="Recruiter email domain diverges from organization website",
                    severity=FindingSeverity.CAUTION,
                    explanation=(
                        f"The recruiter's email domain (@{email_domain}) differs from the stated opportunity website ({org_domain}). "
                        "There is no verified technical link connecting the sender's domain to the hiring organization."
                    ),
                    related_claim_ids=get_claims_by_category("recruiter"),
                    related_evidence_ids=get_evidence_by_type("email_domain_consistency"),
                    why_it_matters=(
                        "Discrepancies between the recruiting email domain and the claimed company domain can indicate "
                        "unauthorized third-party placement agencies, affiliate marketing, or corporate impersonation."
                    ),
                    limitations=(
                        "Legitimate employers often partner with external recruiting agencies, headhunters, or search firms "
                        "that operate from separate business domains."
                    ),
                    recommended_action=(
                        "Verify that the recruiter's agency has an active mandate to hire for the claimed organization by "
                        "contacting the primary employer's human resources department."
                    ),
                )
            )
            finding_num += 1

        # 4. NEWLY REGISTERED DOMAIN (<30 DAYS) (CAUTION)
        new_domain_obs = [o for o in observations if o.finding in ("new_domain", "newly_registered_domain")]
        if new_domain_obs:
            dom_ev = [e for e in evidence if e.evidence_type == "domain_registration"]
            ev_data = getattr(dom_ev[0], "raw_data", None) or getattr(dom_ev[0], "data", None) or {} if dom_ev else {}
            domain = ev_data.get("domain") or getattr(new_domain_obs[0], "target", "Application domain")
            age_days = ev_data.get("age_days", ev_data.get("domain_age_days", 10))
            reg_date = ev_data.get("registration_date", "recent")
            findings.append(
                AssessmentFinding(
                    finding_id=f"FND-{finding_num:03d}",
                    title=f"Application domain is newly registered ({age_days} days old)",
                    severity=FindingSeverity.CAUTION,
                    explanation=(
                        f"The domain '{domain}' was registered only {age_days} days ago (Registration date: {reg_date}). "
                        "Newly created web properties have no established operational track record."
                    ),
                    related_claim_ids=get_claims_by_category("organisation") + get_claims_by_category("application"),
                    related_evidence_ids=get_evidence_by_type("domain_registration"),
                    why_it_matters=(
                        "A substantial portion of deceptive job boards and credential-harvesting pages are hosted on "
                        "newly registered domains that are abandoned within weeks or months."
                    ),
                    limitations=(
                        "Early-stage startups, newly launched student ventures, or rebranded initiatives legitimately "
                        "register new domains. Domain youth is a technical risk signal, not definitive evidence of malpractice."
                    ),
                    recommended_action=(
                        "Cross-reference the domain with verified business filings, active corporate social profiles, "
                        "and established press mentions before submitting resumes or personal information."
                    ),
                )
            )
            finding_num += 1

        # 5. RELATIVELY RECENT DOMAIN (30-180 DAYS) (INFORMATIONAL)
        recent_domain_obs = [o for o in observations if o.finding in ("recent_domain", "relatively_recent_domain")]
        if recent_domain_obs and not new_domain_obs:
            dom_ev = [e for e in evidence if e.evidence_type == "domain_registration"]
            ev_data = getattr(dom_ev[0], "raw_data", None) or getattr(dom_ev[0], "data", None) or {} if dom_ev else {}
            domain = ev_data.get("domain") or getattr(recent_domain_obs[0], "target", "Application domain")
            age_days = ev_data.get("age_days", ev_data.get("domain_age_days", 90))
            findings.append(
                AssessmentFinding(
                    finding_id=f"FND-{finding_num:03d}",
                    title=f"Domain registered relatively recently ({age_days} days old)",
                    severity=FindingSeverity.INFORMATIONAL,
                    explanation=(
                        f"The domain '{domain}' was registered within the past six months ({age_days} days ago). "
                        "It possesses limited historical reputation data on public DNS registries."
                    ),
                    related_claim_ids=get_claims_by_category("organisation"),
                    related_evidence_ids=get_evidence_by_type("domain_registration"),
                    why_it_matters=(
                        "Relatively young domains have less established search presence and reputation history."
                    ),
                    limitations="The domain appears properly registered; age alone does not imply suspicious activity.",
                    recommended_action="Review company background on professional networks and independent directories.",
                )
            )
            finding_num += 1

        # 6. APPLICATION DOMAIN MISMATCH / DIVERGENCE (CAUTION)
        domain_mismatch_obs = [o for o in observations if o.finding in ("domain_mismatch", "domain_divergence")]
        if domain_mismatch_obs:
            url_ev = [e for e in evidence if e.evidence_type == "url_consistency"]
            ev_data = getattr(url_ev[0], "raw_data", None) or getattr(url_ev[0], "data", None) or {} if url_ev else {}
            org_dom = ev_data.get("org_domain", "stated website")
            app_dom = ev_data.get("app_domain", "application portal")
            findings.append(
                AssessmentFinding(
                    finding_id=f"FND-{finding_num:03d}",
                    title="Application destination differs from stated company website",
                    severity=FindingSeverity.CAUTION,
                    explanation=(
                        f"The stated company website domain is '{org_dom}', but the application "
                        f"portal redirects candidates to '{app_dom}'."
                    ),
                    related_claim_ids=get_claims_by_category("application"),
                    related_evidence_ids=get_evidence_by_type("url_consistency"),
                    why_it_matters=(
                        "Diverting applicants to unrelated external domains can be used to bypass corporate security, "
                        "harvest credentials, or collect unauthorized applicant data."
                    ),
                    limitations=(
                        "Legitimate employers frequently utilize trusted applicant tracking platforms (such as "
                        "Greenhouse, Lever, Workday) or hosted forms (Typeform, Google Forms) for hiring."
                    ),
                    recommended_action=(
                        "Ensure the external application link originated from the company's verified careers portal "
                        "rather than an unverified communication."
                    ),
                )
            )
            finding_num += 1

        # 7. RAW IP ADDRESS HOST (CAUTION)
        raw_ip_obs = [o for o in observations if o.finding == "raw_ip_host"]
        if raw_ip_obs:
            findings.append(
                AssessmentFinding(
                    finding_id=f"FND-{finding_num:03d}",
                    title="Application link uses a raw IP address instead of a domain name",
                    severity=FindingSeverity.CAUTION,
                    explanation=(
                        "The application URL points directly to an IP address rather than a named, "
                        "registered organizational domain name."
                    ),
                    related_claim_ids=get_claims_by_category("application"),
                    related_evidence_ids=get_evidence_by_type("url_consistency"),
                    why_it_matters=(
                        "Legitimate organizations host professional recruitment portals on named domains equipped with "
                        "SSL certificates. Raw IP addresses are often used in temporary or malicious infrastructure."
                    ),
                    limitations="Test environments or internal systems may occasionally use raw IP addresses.",
                    recommended_action="Do not enter credentials or submit personal documents to a raw IP address.",
                )
            )
            finding_num += 1

        # 8. UNENCRYPTED HTTP PROTOCOL (CAUTION)
        http_obs = [o for o in observations if o.finding in ("http_only", "http_protocol_unencrypted")]
        if http_obs:
            findings.append(
                AssessmentFinding(
                    finding_id=f"FND-{finding_num:03d}",
                    title="Application URL uses unencrypted HTTP protocol",
                    severity=FindingSeverity.CAUTION,
                    explanation=(
                        "The application link uses plain 'http://' rather than secure 'https://'. Any data transmitted "
                        "across this connection is vulnerable to interception or tampering."
                    ),
                    related_claim_ids=get_claims_by_category("application"),
                    related_evidence_ids=get_evidence_by_type("url_consistency"),
                    why_it_matters="Candidate resumes and personal information should never be sent over cleartext connections.",
                    limitations="Some older informational sites fail to enforce automated HTTPS redirects.",
                    recommended_action="Never input passwords, identification numbers, or bank details on an unencrypted web page.",
                )
            )
            finding_num += 1

        # 9. MISSING MX RECORDS (CAUTION)
        no_mx_obs = [o for o in observations if o.finding in ("no_mx", "no_mx_records")]
        if no_mx_obs:
            findings.append(
                AssessmentFinding(
                    finding_id=f"FND-{finding_num:03d}",
                    title="Target domain lacks configured Mail Exchange (MX) records",
                    severity=FindingSeverity.CAUTION,
                    explanation=(
                        "The target domain does not publish MX records and cannot receive standard email communications."
                    ),
                    related_claim_ids=get_claims_by_category("organisation") + get_claims_by_category("recruiter"),
                    related_evidence_ids=get_evidence_by_type("dns_records"),
                    why_it_matters=(
                        "Operational business domains typically publish MX records to support corporate mailboxes."
                    ),
                    limitations=(
                        "Some organizations use subdomains solely for web hosting while mail is handled on a parent domain."
                    ),
                    recommended_action="Confirm whether the organization uses a different corporate domain for its email correspondence.",
                )
            )
            finding_num += 1

        # 10. SUSPICIOUS LINGUISTIC INDICATORS (CAUTION)
        suspicious_phrases = []
        indicators_list = suspicious_indicators or getattr(extracted_info, "suspicious_indicators", []) or []
        for ind in indicators_list:
            phrase = getattr(ind, "phrase", None) or getattr(ind, "statement", "")
            cat = getattr(ind, "category", None) or getattr(ind, "indicator_type", "linguistic")
            if not any(kw in cat.lower() or kw in phrase.lower() for kw in ("fee", "payment", "money")):
                suspicious_phrases.append(f"'{phrase}' ({cat})")

        for c in claims:
            if (c.claim_category or "").lower() == "suspicious_indicator":
                if not any(kw in c.claim_text.lower() for kw in ("fee", "payment", "money")):
                    suspicious_phrases.append(f"'{c.claim_text}'")

        if suspicious_phrases:
            phrase_summary = ", ".join(suspicious_phrases[:3])
            findings.append(
                AssessmentFinding(
                    finding_id=f"FND-{finding_num:03d}",
                    title="Urgency, guaranteed-selection, or pressure language detected",
                    severity=FindingSeverity.CAUTION,
                    explanation=(
                        f"The announcement employs suspicious marketing or pressure phrasing: {phrase_summary}. "
                        "Phrases such as 'guaranteed selection', immediate deadlines, or 'no interview required' "
                        "are frequently used to bypass candidates' critical scrutiny."
                    ),
                    related_claim_ids=get_claims_by_category("suspicious_indicator"),
                    related_evidence_ids=[],
                    why_it_matters=(
                        "Legitimate hiring processes incorporate objective skills assessments and interviews. "
                        "Unrealistic guarantees are designed to evoke quick compliance before candidates verify facts."
                    ),
                    limitations=(
                        "Aggressive marketing or informal recruitment copy can sometimes produce sensational phrasing "
                        "without fraudulent intent."
                    ),
                    recommended_action=(
                        "Insist on standard evaluation steps: a formal interview, detailed job descriptions, and "
                        "direct contact with the hiring manager before accepting any offer."
                    ),
                )
            )
            finding_num += 1

        return findings

    # -------------------------------------------------------------------------
    # Private Helpers: Category Determination
    # -------------------------------------------------------------------------
    def _determine_assessment_level(
        self,
        extracted_info: Optional[ExtractedInformation],
        claims: List[ClaimItem],
        evidence: List[EvidenceItem],
        observations: List[TechnicalObservation],
        findings: List[AssessmentFinding],
    ) -> tuple[AssessmentLevel, str, str]:
        # Count severities
        high_severity_count = sum(1 for f in findings if f.severity == FindingSeverity.HIGH_CAUTION)
        caution_count = sum(1 for f in findings if f.severity == FindingSeverity.CAUTION)

        # Check for insufficient evidence conditions:
        has_org_website = False
        has_recruiter_email = False
        if extracted_info:
            if extracted_info.organisation and extracted_info.organisation.website:
                has_org_website = True
            if extracted_info.recruiter and extracted_info.recruiter.email:
                has_recruiter_email = True

        available_evidence_count = sum(1 for e in evidence if e.status == "available")
        is_sparse_opportunity = (not has_org_website and not has_recruiter_email and available_evidence_count == 0)

        # Rule A: High Caution
        # Triggers on explicit fee requests OR multiple independent warning indicators
        if high_severity_count >= 1 or caution_count >= 2:
            level = AssessmentLevel.HIGH_CAUTION
            label = "High caution"
            if high_severity_count >= 1:
                summary = (
                    "High caution recommended. An upfront registration, processing, or training fee was requested. "
                    "Upfront recruitment or processing fees are a significant warning sign. "
                    "Independently confirm the request through the organisation's official channels before paying."
                )
            else:
                summary = (
                    "High caution recommended. Multiple independent technical and linguistic warning indicators were detected "
                    "(e.g., domain youth, free email usage, or pressure language). Exercise extreme diligence."
                )
            return level, label, summary

        # Rule B: Insufficient Evidence (when sparse and no critical fee found)
        if is_sparse_opportunity or (len(claims) <= 1 and available_evidence_count == 0):
            # Check if there were any caution findings
            if caution_count == 0:
                level = AssessmentLevel.INSUFFICIENT_EVIDENCE
                label = "Insufficient evidence"
                summary = (
                    "Insufficient verifiable information provided. The opportunity announcement did not include an official website, "
                    "a verifiable recruiter email address, or sufficient technical identifiers to perform cross-referencing. "
                    "Request complete organizational details before proceeding."
                )
                return level, label, summary

        # Rule C: Needs Careful Review
        # Triggers when there is at least one meaningful warning indicator
        if caution_count >= 1:
            level = AssessmentLevel.NEEDS_CAREFUL_REVIEW
            label = "Needs careful review"
            summary = (
                "Needs careful review. One or more meaningful warning indicators or unresolved technical inconsistencies "
                "(such as free webmail recruitment, recently registered domain, or pressure phrasing) require independent confirmation."
            )
            return level, label, summary

        # Rule D: Limited Concerns Detected
        # Triggers when sufficient checks were performed and no high caution or caution indicators were found
        level = AssessmentLevel.LIMITED_CONCERNS_DETECTED
        label = "Limited concerns detected"
        summary = (
            "Limited concerns detected during technical checks. Available domain registration, DNS records, and email formatting "
            "were consistent with standard operations. IMPORTANT: Technical consistency does not verify that the opportunity "
            "or organization is genuine. Always independently verify vacancies directly on the employer's official careers portal."
        )
        return level, label, summary


assessment_service = AssessmentService()
