import sys
import asyncio
from pathlib import Path
from typing import Optional, Dict, Any, List
from unittest.mock import patch, MagicMock

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
)
from app.schemas.verification import VerificationRequest, AnalyzeRequest
from app.services.evidence.base import (
    normalize_hostname,
    is_safe_public_hostname,
    extract_registrable_domain,
    VerificationContext,
)
from app.services.evidence.domain_service import DomainIntelligenceProvider
from app.services.evidence.dns_service import DNSIntelligenceProvider
from app.services.evidence.email_service import EmailDomainConsistencyProvider
from app.services.evidence.url_service import URLConsistencyProvider
from app.services.evidence.organisation_service import OrganisationIdentityConsistencyProvider
from app.services.verification_service import VerificationService


def test_hostname_normalization_and_registrable_domain():
    # Test normalization from URL
    assert normalize_hostname("https://careers.google.co.uk/jobs/123") == "careers.google.co.uk"
    assert extract_registrable_domain("careers.google.co.uk") == "google.co.uk"

    # Test normalization from email
    assert normalize_hostname("recruiter@apextechnologies.com") == "apextechnologies.com"
    assert extract_registrable_domain("apextechnologies.com") == "apextechnologies.com"

    # Subdomain extraction
    assert extract_registrable_domain("sub.portal.example.com") == "example.com"
    print("[PASS] Hostname normalization and registrable domain tests passed.")


def test_hostname_security_and_private_ip_rejection():
    # Safe public domains
    assert is_safe_public_hostname("google.com") is True
    assert is_safe_public_hostname("careers.apex-tech.io") is True
    assert is_safe_public_hostname("example.co.uk") is True

    # Reject localhost and internal network
    assert is_safe_public_hostname("localhost") is False
    assert is_safe_public_hostname("localhost.localdomain") is False
    assert is_safe_public_hostname("server.local") is False
    assert is_safe_public_hostname("intranet.internal") is False

    # Reject private IPv4 (RFC 1918) and loopback
    assert is_safe_public_hostname("127.0.0.1") is False
    assert is_safe_public_hostname("10.0.0.1") is False
    assert is_safe_public_hostname("192.168.1.1") is False
    assert is_safe_public_hostname("172.16.0.1") is False

    # Reject AWS/cloud metadata address
    assert is_safe_public_hostname("169.254.169.254") is False

    # Reject single-label / invalid format
    assert is_safe_public_hostname("singleword") is False
    assert is_safe_public_hostname("invalid..domain.com") is False
    print("[PASS] Private IP and localhost security filtering passed.")


async def test_email_domain_consistency():
    provider = EmailDomainConsistencyProvider()

    # 1. Matching domain
    info_match = ExtractedInformation(
        organisation=OrganisationInfo(name="Apex Corp", website="https://apexcorp.com"),
        recruiter=RecruiterInfo(email="recruiter@apexcorp.com"),
    )
    ctx_match = VerificationContext(info_match)
    _, obs_match = await provider.collect(ctx_match)
    assert any(o.finding == "matching_domain" for o in obs_match)

    # 2. Free consumer email provider
    info_free = ExtractedInformation(
        organisation=OrganisationInfo(name="Global Technologies", website="https://globaltech.io"),
        recruiter=RecruiterInfo(email="hiring.manager@gmail.com"),
    )
    ctx_free = VerificationContext(info_free)
    _, obs_free = await provider.collect(ctx_free)
    assert any(o.finding == "free_email_provider" for o in obs_free)

    # 3. Different corporate domain
    info_diff = ExtractedInformation(
        organisation=OrganisationInfo(name="Apex Corp", website="https://apexcorp.com"),
        recruiter=RecruiterInfo(email="recruiter@external-agency.net"),
    )
    ctx_diff = VerificationContext(info_diff)
    _, obs_diff = await provider.collect(ctx_diff)
    assert any(o.finding == "different_domain" for o in obs_diff)

    print("[PASS] Email domain consistency (matching, free provider, mismatch) passed.")


async def test_url_consistency_analysis():
    provider = URLConsistencyProvider()

    # 1. HTTPS and matching subdomain
    info_sub = ExtractedInformation(
        organisation=OrganisationInfo(website="https://apex.com"),
        application=ApplicationInfo(application_url="https://careers.apex.com/apply"),
    )
    ctx_sub = VerificationContext(info_sub, application_url="https://careers.apex.com/apply")
    ev_sub, obs_sub = await provider.collect(ctx_sub)
    assert any(o.finding == "https" for o in obs_sub)
    assert any("subdomain of the primary organization domain" in ev.interpretation for ev in ev_sub)

    # 2. HTTP only (unencrypted)
    info_http = ExtractedInformation(
        application=ApplicationInfo(application_url="http://unsecured-portal.com/apply"),
    )
    ctx_http = VerificationContext(info_http, application_url="http://unsecured-portal.com/apply")
    _, obs_http = await provider.collect(ctx_http)
    assert any(o.finding == "http_only" for o in obs_http)

    print("[PASS] URL consistency and transport security inspection passed.")


async def test_mocked_domain_rdap_provider():
    provider = DomainIntelligenceProvider()
    info = ExtractedInformation(organisation=OrganisationInfo(website="https://abctechnologies.com"))
    ctx = VerificationContext(info)

    # Mock RDAP 200 response with registration date 45 days ago
    mock_rdap_payload = {
        "events": [
            {"eventAction": "registration", "eventDate": "2026-09-15T10:00:00Z"},
            {"eventAction": "last changed", "eventDate": "2026-10-01T12:00:00Z"},
        ],
        "entities": [
            {"roles": ["registrar"], "handle": "GoDaddy Online LLC"}
        ],
        "status": ["clientTransferProhibited", "active"],
    }

    class MockResponse:
        status_code = 200
        def json(self):
            return mock_rdap_payload

    with patch("httpx.AsyncClient.get", return_value=MockResponse()):
        ev_list, obs_list = await provider.collect(ctx)
        assert len(ev_list) == 1
        ev = ev_list[0]
        assert ev.status == "available"
        assert "days old" in ev.observed_value
        assert any(o.finding == "recent_domain" for o in obs_list)
        assert len(ev.limitations) >= 1

    # Mock RDAP 404 response
    class Mock404Response:
        status_code = 404
        def json(self):
            return {}

    with patch("httpx.AsyncClient.get", return_value=Mock404Response()):
        ev_404, obs_404 = await provider.collect(ctx)
        assert ev_404[0].status == "not_available"
        assert any(o.finding == "rdap_not_found" for o in obs_404)

    print("[PASS] Mocked RDAP intelligence tests (success, recent domain, 404) passed.")


async def test_mocked_dns_doh_provider():
    provider = DNSIntelligenceProvider()
    info = ExtractedInformation(organisation=OrganisationInfo(website="https://apexcorp.com"))
    ctx = VerificationContext(info)

    async def mock_doh_query(target, rtype, type_code):
        if rtype == "A":
            return ["93.184.216.34"]
        elif rtype == "MX":
            return ["10 mail.apexcorp.com"]
        elif rtype == "NS":
            return ["ns1.apexcorp.com", "ns2.apexcorp.com"]
        elif rtype == "TXT":
            return ["v=spf1 include:_spf.google.com ~all"]
        return []

    with patch.object(provider, "_query_doh_record", side_effect=mock_doh_query):
        ev_list, obs_list = await provider.collect(ctx)
        assert len(ev_list) == 1
        ev = ev_list[0]
        assert ev.status == "available"
        assert "93.184.216.34" in ev.observed_value
        assert any(o.finding == "has_mx" for o in obs_list)
        assert any("SPF" in ev.interpretation for ev in ev_list)

    print("[PASS] Mocked DNS DoH provider tests (A, MX, NS, TXT) passed.")


async def test_verification_service_claim_mapping():
    """
    Verifies that claims are accurately classified without inflating verdicts:
    - Financial & Opportunity claims MUST remain strictly 'not_checked'.
    - Organisation & Email claims receive 'inconclusive' when technical signals are observed.
    """
    service = VerificationService()

    info = ExtractedInformation(
        organisation=OrganisationInfo(name="ABC Technologies", website="https://abctech.example.com"),
        opportunity=OpportunityInfo(role="Data Science Intern"),
        financial_details=FinancialDetails(stipend="₹45,000 per month", registration_fees="₹1,500"),
        recruiter=RecruiterInfo(email="recruiter@gmail.com"),
    )

    claims = [
        ClaimItem(
            claim_id="CLM-001",
            claim_text="Organisation claims to be ABC Technologies.",
            claim_category="organisation",
            source_text="at ABC Technologies",
            verification_status="not_checked",
        ),
        ClaimItem(
            claim_id="CLM-002",
            claim_text="Organisation claims to offer a Data Science Intern position.",
            claim_category="opportunity",
            source_text="Selected for Data Science Intern",
            verification_status="not_checked",
        ),
        ClaimItem(
            claim_id="CLM-003",
            claim_text="Advertised monthly stipend is ₹45,000 per month.",
            claim_category="financial",
            source_text="Earn ₹45,000 per month",
            verification_status="not_checked",
        ),
        ClaimItem(
            claim_id="CLM-004",
            claim_text="Applicant is asked to pay ₹1,500 as a registration fee.",
            claim_category="financial",
            source_text="Pay ₹1,500 as a registration fee",
            verification_status="not_checked",
        ),
        ClaimItem(
            claim_id="CLM-005",
            claim_text="Recruiter email is stated as recruiter@gmail.com.",
            claim_category="recruiter",
            source_text="recruiter@gmail.com",
            verification_status="not_checked",
        ),
    ]

    req = VerificationRequest(
        extracted_information=info,
        claims=claims,
        source_type="text",
        application_url="https://abctech.example.com/apply",
    )

    res = await service.verify(req)
    assert res.success is True
    assert len(res.claims) == 5
    assert len(res.evidence) >= 4

    claim_map = {c.claim_id: c for c in res.claims}

    # Financial and Opportunity claims MUST be strictly 'not_checked'
    assert claim_map["CLM-002"].verification_status == "not_checked"
    assert "cannot be verified through technical network signals" in claim_map["CLM-002"].verification_explanation

    assert claim_map["CLM-003"].verification_status == "not_checked"
    assert "cannot be verified through DNS" in claim_map["CLM-003"].verification_explanation

    assert claim_map["CLM-004"].verification_status == "not_checked"

    # Recruiter free email claim should be inconclusive with linked evidence
    assert claim_map["CLM-005"].verification_status == "inconclusive"
    assert len(claim_map["CLM-005"].evidence_ids) >= 1

    # Summary checks
    assert res.verification_summary.not_checked >= 3
    assert res.verification_summary.supported == 0  # Technical DNS cannot certify genuine jobs
    assert res.verification_summary.contradicted == 0

    print("[PASS] Verification claim-to-evidence mapping and status integrity passed.")


async def main():
    test_hostname_normalization_and_registrable_domain()
    test_hostname_security_and_private_ip_rejection()
    await test_email_domain_consistency()
    await test_url_consistency_analysis()
    await test_mocked_domain_rdap_provider()
    await test_mocked_dns_doh_provider()
    await test_verification_service_claim_mapping()
    print("\nALL PHASE 3 VERIFICATION TESTS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    asyncio.run(main())
