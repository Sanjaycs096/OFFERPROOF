import sys
from pathlib import Path
from datetime import datetime, timezone

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from app.schemas.extraction import (
    ExtractedInformation,
    OrganisationInfo,
    OpportunityInfo,
    FinancialDetails,
    RecruiterInfo,
    ApplicationInfo,
    ClaimItem,
    SuspiciousIndicator,
)
from app.schemas.evidence import EvidenceItem, TechnicalObservation
from app.schemas.verification import VerificationSummary
from app.schemas.assessment import (
    AssessmentLevel,
    FindingSeverity,
    AssessmentRequest,
    AssessmentResponse,
)
from app.services.assessment_service import assessment_service


def test_upfront_fee_triggers_high_caution():
    """Explicit upfront fee request must deterministically trigger high_caution."""
    extracted_info = ExtractedInformation(
        organisation=OrganisationInfo(name="ScamCorp", website="https://scamcorp.example.com"),
        opportunity=OpportunityInfo(title="Junior Data Analyst", category="job"),
        financial_details=FinancialDetails(
            salary="$60/hr",
            registration_fees="$150 onboarding fee",
        ),
        recruiter=RecruiterInfo(name="John Doe", email="hr@scamcorp.example.com"),
    )
    claims = [
        ClaimItem(
            claim_id="CLM-001",
            claim_text="Organisation is ScamCorp.",
            claim_category="organisation",
            source_text="ScamCorp",
            confidence=0.9,
            verification_status="inconclusive",
        ),
        ClaimItem(
            claim_id="CLM-002",
            claim_text="Candidate must pay $150 onboarding fee.",
            claim_category="financial",
            source_text="$150 onboarding fee",
            confidence=0.95,
            verification_status="not_checked",
        ),
    ]
    report = assessment_service.generate_assessment(
        extracted_info=extracted_info,
        claims=claims,
        evidence=[],
        observations=[],
    )
    assert report.assessment.assessment_level == AssessmentLevel.HIGH_CAUTION
    assert report.assessment.assessment_label == "High caution"
    assert any(f.severity == FindingSeverity.HIGH_CAUTION for f in report.findings)
    assert any("fee" in f.title.lower() for f in report.findings)

    # Must contain payment safety recommendation
    has_payment_rec = any(r.topic == "payment_safety" for r in report.recommendations)
    assert has_payment_rec is True

    # Financial claim must be recorded as unverified
    unverified_ids = [u.claim_id for u in report.unverified_claims]
    assert "CLM-002" in unverified_ids
    print("[PASS] test_upfront_fee_triggers_high_caution passed.")


def test_multiple_independent_warnings_triggers_high_caution():
    """Multiple independent warnings (e.g. free email + newly registered domain) -> high_caution."""
    extracted_info = ExtractedInformation(
        organisation=OrganisationInfo(name="NewStartup", website="https://newstartup-apply.xyz"),
        opportunity=OpportunityInfo(title="Software Intern", category="internship"),
        recruiter=RecruiterInfo(name="Jane Recruiter", email="newstartup.hr@gmail.com"),
    )
    claims = [
        ClaimItem(
            claim_id="CLM-001",
            claim_text="Recruiter email is newstartup.hr@gmail.com",
            claim_category="recruiter",
            source_text="newstartup.hr@gmail.com",
            confidence=0.9,
            verification_status="inconclusive",
        ),
        ClaimItem(
            claim_id="CLM-002",
            claim_text="Website is https://newstartup-apply.xyz",
            claim_category="organisation",
            source_text="https://newstartup-apply.xyz",
            confidence=0.9,
            verification_status="inconclusive",
        ),
    ]
    evidence = [
        EvidenceItem(
            evidence_id="ev_dom_01",
            evidence_type="domain_registration",
            source_name="RDAP Directory",
            retrieved_at=datetime.now(timezone.utc),
            status="available",
            observed_value="Registered 10 days ago",
            interpretation="Domain is newly registered (< 30 days)",
            raw_data={"domain": "newstartup-apply.xyz", "age_days": 10, "registration_date": "2026-10-21"},
        ),
        EvidenceItem(
            evidence_id="ev_email_01",
            evidence_type="email_domain_consistency",
            source_name="Email Domain Analysis",
            retrieved_at=datetime.now(timezone.utc),
            status="available",
            observed_value="Free email provider gmail.com",
            interpretation="Recruiter uses consumer webmail",
            raw_data={"recruiter_email": "newstartup.hr@gmail.com", "consistency_type": "free_email_provider"},
        ),
    ]
    observations = [
        TechnicalObservation(
            observation_id="obs_01",
            category="domain",
            finding="new_domain",
            label="Newly Registered Domain",
            detail="Domain was registered 10 days ago.",
            severity="notable",
        ),
        TechnicalObservation(
            observation_id="obs_02",
            category="email",
            finding="free_email_provider",
            label="Free Webmail Recruiter",
            detail="Recruiter uses gmail.com",
            severity="notable",
        ),
    ]
    report = assessment_service.generate_assessment(
        extracted_info=extracted_info,
        claims=claims,
        evidence=evidence,
        observations=observations,
    )
    assert report.assessment.assessment_level == AssessmentLevel.HIGH_CAUTION
    assert len(report.findings) >= 2
    # Verify evidence references
    all_ev_ids = [eid for f in report.findings for eid in f.related_evidence_ids]
    assert "ev_dom_01" in all_ev_ids
    assert "ev_email_01" in all_ev_ids
    print("[PASS] test_multiple_independent_warnings_triggers_high_caution passed.")


def test_single_warning_triggers_needs_careful_review():
    """A single caution warning (e.g. free email on established domain) -> needs_careful_review."""
    extracted_info = ExtractedInformation(
        organisation=OrganisationInfo(name="Acme Corp", website="https://acmecorp.example.com"),
        recruiter=RecruiterInfo(name="Recruiter Bob", email="acme.recruiter@yahoo.com"),
    )
    claims = [
        ClaimItem(
            claim_id="CLM-001",
            claim_text="Contact email is acme.recruiter@yahoo.com",
            claim_category="recruiter",
            source_text="acme.recruiter@yahoo.com",
            confidence=0.85,
            verification_status="inconclusive",
        )
    ]
    observations = [
        TechnicalObservation(
            observation_id="obs_01",
            category="email",
            finding="free_email_provider",
            label="Free Email Provider",
            detail="Recruiter uses public webmail yahoo.com",
            severity="notable",
        )
    ]
    report = assessment_service.generate_assessment(
        extracted_info=extracted_info,
        claims=claims,
        evidence=[],
        observations=observations,
    )
    assert report.assessment.assessment_level == AssessmentLevel.NEEDS_CAREFUL_REVIEW
    assert report.assessment.assessment_label == "Needs careful review"
    assert len(report.findings) == 1
    assert report.findings[0].severity == FindingSeverity.CAUTION
    print("[PASS] test_single_warning_triggers_needs_careful_review passed.")


def test_clean_opportunity_triggers_limited_concerns():
    """Clean opportunity with established domain, corporate email, and no red flags -> limited_concerns_detected."""
    extracted_info = ExtractedInformation(
        organisation=OrganisationInfo(name="Enterprise Global", website="https://enterpriseglobal.example.com"),
        opportunity=OpportunityInfo(title="Security Analyst", category="job"),
        recruiter=RecruiterInfo(name="Alice HR", email="hr@enterpriseglobal.example.com"),
    )
    claims = [
        ClaimItem(
            claim_id="CLM-001",
            claim_text="Enterprise Global website is https://enterpriseglobal.example.com",
            claim_category="organisation",
            source_text="https://enterpriseglobal.example.com",
            confidence=0.9,
            verification_status="inconclusive",
        ),
        ClaimItem(
            claim_id="CLM-002",
            claim_text="Recruiter email is hr@enterpriseglobal.example.com",
            claim_category="recruiter",
            source_text="hr@enterpriseglobal.example.com",
            confidence=0.9,
            verification_status="inconclusive",
        ),
    ]
    evidence = [
        EvidenceItem(
            evidence_id="ev_01",
            evidence_type="domain_registration",
            source_name="RDAP Directory",
            retrieved_at=datetime.now(timezone.utc),
            status="available",
            observed_value="Registered 1,200 days ago",
            interpretation="Established domain (> 180 days)",
            raw_data={"domain": "enterpriseglobal.example.com", "age_days": 1200, "registration_date": "2023-01-01"},
        ),
        EvidenceItem(
            evidence_id="ev_02",
            evidence_type="dns_records",
            source_name="Cloudflare DoH",
            retrieved_at=datetime.now(timezone.utc),
            status="available",
            observed_value="Active A and MX records",
            interpretation="DNS configuration valid",
            raw_data={"hostname": "enterpriseglobal.example.com", "a_records": ["93.184.216.34"], "mx_records": ["mail.enterpriseglobal.example.com"]},
        ),
    ]
    # No caution observations
    report = assessment_service.generate_assessment(
        extracted_info=extracted_info,
        claims=claims,
        evidence=evidence,
        observations=[],
    )
    assert report.assessment.assessment_level == AssessmentLevel.LIMITED_CONCERNS_DETECTED
    assert report.assessment.assessment_label == "Limited concerns detected"
    # Mandatory disclaimer must be present
    assert "never" in report.assessment.summary.lower() or "not verify" in report.assessment.summary.lower()
    assert len(report.verified_facts) >= 2
    print("[PASS] test_clean_opportunity_triggers_limited_concerns passed.")


def test_insufficient_evidence():
    """Opportunity with no website, no recruiter email, and sparse claims -> insufficient_evidence."""
    extracted_info = ExtractedInformation(
        organisation=OrganisationInfo(name=None, website=None),
        opportunity=OpportunityInfo(title="Vague Gig", category="job"),
    )
    claims = [
        ClaimItem(
            claim_id="CLM-001",
            claim_text="Vague gig offering.",
            claim_category="opportunity",
            source_text="Vague gig offering.",
            confidence=0.5,
            verification_status="not_checked",
        )
    ]
    report = assessment_service.generate_assessment(
        extracted_info=extracted_info,
        claims=claims,
        evidence=[],
        observations=[],
    )
    assert report.assessment.assessment_level == AssessmentLevel.INSUFFICIENT_EVIDENCE
    assert report.assessment.assessment_label == "Insufficient evidence"
    assert any("insufficient" in s.action.lower() or "website" in s.action.lower() for s in report.next_steps)
    print("[PASS] test_insufficient_evidence passed.")


def test_external_provider_failures_graceful_handling():
    """If external evidence providers are empty/failed, assessment produces a valid response without crashing."""
    extracted_info = ExtractedInformation(
        organisation=OrganisationInfo(name="Timeout Corp", website="https://timeout-corp.example.com"),
    )
    claims = [
        ClaimItem(
            claim_id="CLM-001",
            claim_text="Timeout Corp exists.",
            claim_category="organisation",
            source_text="Timeout Corp",
            confidence=0.8,
            verification_status="not_checked",
        )
    ]
    report = assessment_service.generate_assessment(
        extracted_info=extracted_info,
        claims=claims,
        evidence=[],
        observations=[],
    )
    assert report.assessment is not None
    assert isinstance(report.findings, list)
    assert isinstance(report.recommendations, list)
    assert isinstance(report.next_steps, list)
    print("[PASS] test_external_provider_failures_graceful_handling passed.")


def test_deterministic_results():
    """Running assessment on identical inputs produces identical deterministic results."""
    extracted_info = ExtractedInformation(
        organisation=OrganisationInfo(name="Repeat Tech", website="https://repeat-tech.example.com"),
        financial_details=FinancialDetails(salary="$75,000", registration_fees="$100"),
        recruiter=RecruiterInfo(name="Mr Smith", email="smith@gmail.com"),
    )
    claims = [
        ClaimItem(
            claim_id="CLM-001",
            claim_text="Pay $100 fee.",
            claim_category="financial",
            source_text="$100 fee",
            confidence=0.9,
            verification_status="not_checked",
        )
    ]
    obs = [
        TechnicalObservation(
            observation_id="obs_01",
            category="email",
            finding="free_email_provider",
            label="Free Webmail",
            detail="Using gmail.com",
            severity="notable",
        )
    ]
    rep1 = assessment_service.generate_assessment(
        extracted_info=extracted_info,
        claims=claims,
        evidence=[],
        observations=obs,
    )
    rep2 = assessment_service.generate_assessment(
        extracted_info=extracted_info,
        claims=claims,
        evidence=[],
        observations=obs,
    )
    assert rep1.assessment.assessment_level == rep2.assessment.assessment_level
    assert [f.finding_id for f in rep1.findings] == [f.finding_id for f in rep2.findings]
    assert [r.title for r in rep1.recommendations] == [r.title for r in rep2.recommendations]
    print("[PASS] test_deterministic_results passed.")


def test_no_fabricated_evidence_and_traceability():
    """Verified facts must map 1:1 to real available evidence artifacts; no hallucinations."""
    evidence = [
        EvidenceItem(
            evidence_id="ev_real_01",
            evidence_type="domain_registration",
            source_name="RDAP Directory",
            retrieved_at=datetime.now(timezone.utc),
            status="available",
            observed_value="Registered 45 days ago",
            interpretation="Recent domain",
            raw_data={"domain": "verifiable-target.com", "age_days": 45, "registration_date": "2026-09-15"},
        )
    ]
    report = assessment_service.generate_assessment(
        extracted_info=None,
        claims=[],
        evidence=evidence,
        observations=[],
    )
    # Exactly 1 verified fact created
    assert len(report.verified_facts) == 1
    assert report.verified_facts[0].source_name == "RDAP Directory"
    assert "verifiable-target.com" in report.verified_facts[0].statement
    print("[PASS] test_no_fabricated_evidence_and_traceability passed.")


def main():
    print("Running Phase 4 Assessment Unit Tests...\n")
    test_upfront_fee_triggers_high_caution()
    test_multiple_independent_warnings_triggers_high_caution()
    test_single_warning_triggers_needs_careful_review()
    test_clean_opportunity_triggers_limited_concerns()
    test_insufficient_evidence()
    test_external_provider_failures_graceful_handling()
    test_deterministic_results()
    test_no_fabricated_evidence_and_traceability()
    print("\n[PASS] ALL PHASE 4 ASSESSMENT TESTS COMPLETED SUCCESSFULLY!")


if __name__ == "__main__":
    main()
