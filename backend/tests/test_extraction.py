import sys
import asyncio
from pathlib import Path
from typing import Optional, Dict, Any

backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from app.schemas.extraction import ExtractionRequest
from app.services.fallback_extractor import fallback_extractor
from app.services.extraction_service import ExtractionService
from app.services.ai_service import BaseAIProvider


class MockFailingAIProvider(BaseAIProvider):
    """Simulates an AI provider that times out or throws an error."""
    @property
    def provider_name(self) -> str:
        return "mock_failing"

    @property
    def is_configured(self) -> bool:
        return True

    async def extract_claims_and_entities(
        self, text: str, application_url: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        raise TimeoutError("Provider gateway timed out after 25s.")


class MockMalformedAIProvider(BaseAIProvider):
    """Simulates an AI provider returning corrupt or schema-invalid data."""
    @property
    def provider_name(self) -> str:
        return "mock_malformed"

    @property
    def is_configured(self) -> bool:
        return True

    async def extract_claims_and_entities(
        self, text: str, application_url: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        # Missing required fields or completely corrupted dictionary
        return {"garbage_field": 12345, "invalid": True}


class MockSuccessfulAIProvider(BaseAIProvider):
    """Simulates a successful AI provider returning structured claims."""
    @property
    def provider_name(self) -> str:
        return "mock_gemini"

    @property
    def is_configured(self) -> bool:
        return True

    async def extract_claims_and_entities(
        self, text: str, application_url: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        return {
            "extracted_information": {
                "organisation": {
                    "name": "Global AI Labs",
                    "website": "https://globalailabs.example.com",
                    "organisation_type": "corporate_entity",
                },
                "opportunity": {
                    "title": "Machine Learning Intern",
                    "category": "internship",
                    "role": "Machine Learning Intern",
                    "required_qualifications": ["Enrolled in B.Tech Computer Science"],
                    "required_skills": ["Python", "PyTorch"],
                    "work_arrangement": "remote",
                    "location": "Remote",
                    "duration": "3 months",
                    "application_deadline": "November 15, 2026",
                },
                "financial_details": {
                    "salary": None,
                    "stipend": "₹50,000 per month",
                    "registration_fees": None,
                    "training_fees": None,
                    "processing_fees": None,
                    "other_payment_requests": [],
                },
                "recruiter": {
                    "name": "Sarah Connor",
                    "email": "sarah.connor@globalailabs.example.com",
                    "phone": None,
                    "contact_info": "@sarah_recruiter",
                },
                "application": {
                    "application_url": "https://globalailabs.example.com/careers/apply",
                    "application_email": "careers@globalailabs.example.com",
                    "application_instructions": "Submit CV and GitHub profile.",
                },
            },
            "claims": [
                {
                    "claim_id": "CLM-001",
                    "claim_text": "Organisation claims to offer a Machine Learning Intern position.",
                    "claim_category": "opportunity",
                    "extracted_value": "Machine Learning Intern",
                    "source_text": "Selected for Machine Learning Intern",
                    "confidence": 0.95,
                    "verification_status": "not_checked",
                },
                {
                    "claim_id": "CLM-002",
                    "claim_text": "Advertised monthly stipend is ₹50,000 per month.",
                    "claim_category": "financial",
                    "extracted_value": "₹50,000 per month",
                    "source_text": "Earn ₹50,000 per month",
                    "confidence": 0.92,
                    "verification_status": "not_checked",
                },
            ],
            "suspicious_indicators": [],
        }


def test_rule_based_extraction_sample():
    sample = (
        "Congratulations! You have been selected for a Data Science Internship at ABC Technologies. "
        "Earn ₹45,000 per month. Pay ₹1,500 as a registration fee before October 31. Guaranteed selection."
    )
    res = fallback_extractor.extract(sample, application_url="https://abctech.example.com/apply")

    assert res.extraction_mode == "rule_based"
    assert res.extracted_information.organisation.name == "ABC Technologies"
    assert res.extracted_information.opportunity.role == "Data Science Internship"
    assert "₹45,000" in res.extracted_information.financial_details.stipend
    assert "₹1,500" in res.extracted_information.financial_details.registration_fees
    assert res.extracted_information.opportunity.application_deadline == "October 31"
    assert res.url_metadata.hostname == "abctech.example.com"

    # Verify all claims are not_checked
    assert len(res.claims) >= 5
    for claim in res.claims:
        assert claim.verification_status == "not_checked", f"Claim {claim.claim_id} status must be 'not_checked'"

    # Verify suspicious indicators
    assert any(ind.indicator_type == "guaranteed_selection" for ind in res.suspicious_indicators)
    print("[PASS] Rule-based sample extraction and claim verification passed.")


def test_email_and_phone_extraction():
    sample = (
        "Contact Senior Recruiter David Miller at david.m@verified-tech.io or +1 (555) 234-5678. "
        "Apply at https://verified-tech.io/careers/4892."
    )
    res = fallback_extractor.extract(sample)
    assert res.extracted_information.recruiter.email == "david.m@verified-tech.io"
    assert res.extracted_information.recruiter.phone is not None
    assert "david.m@verified-tech.io" in [c.extracted_value for c in res.claims if c.extracted_value]
    print("[PASS] Recruiter email and phone extraction passed.")


def test_missing_optional_fields_handled_gracefully():
    sparse_sample = "Just an informal note about some generic opening."
    res = fallback_extractor.extract(sparse_sample)
    assert res.success is True
    assert res.extracted_information.organisation.name is None
    assert res.extracted_information.financial_details.salary is None
    assert res.extraction_summary.total_claims >= 0
    print("[PASS] Sparse content without optional fields handled gracefully.")


async def test_ai_provider_success():
    service = ExtractionService(ai_provider=MockSuccessfulAIProvider())
    req = ExtractionRequest(content="Testing AI extraction pipeline")
    res = await service.extract(req)
    assert res.success is True
    assert res.extraction_mode == "ai"
    assert res.extracted_information.organisation.name == "Global AI Labs"
    assert len(res.claims) == 2
    for c in res.claims:
        assert c.verification_status == "not_checked"
    print("[PASS] Successful AI provider pipeline passed.")


async def test_ai_provider_failure_fallback():
    """When AI provider times out, system must gracefully fall back to rule-based."""
    service = ExtractionService(ai_provider=MockFailingAIProvider())
    req = ExtractionRequest(
        content="Offer from Nexus Corp. Earn $80,000 per year as Junior Analyst. Contact hr@nexuscorp.com."
    )
    res = await service.extract(req)
    assert res.success is True
    assert res.extraction_mode == "rule_based"
    assert res.errors is not None  # Notes fallback
    assert res.extracted_information.recruiter.email == "hr@nexuscorp.com"
    for c in res.claims:
        assert c.verification_status == "not_checked"
    print("[PASS] AI failure fallback to rule-based passed.")


async def test_ai_provider_malformed_json_fallback():
    """When AI provider returns invalid schema, system must fall back to rule-based."""
    service = ExtractionService(ai_provider=MockMalformedAIProvider())
    req = ExtractionRequest(
        content="Scholarship offer at Oxford Foundation. Value: £5,000 per year."
    )
    res = await service.extract(req)
    assert res.success is True
    assert res.extraction_mode == "rule_based"
    for c in res.claims:
        assert c.verification_status == "not_checked"
    print("[PASS] AI malformed response fallback to rule-based passed.")


async def main():
    test_rule_based_extraction_sample()
    test_email_and_phone_extraction()
    test_missing_optional_fields_handled_gracefully()
    await test_ai_provider_success()
    await test_ai_provider_failure_fallback()
    await test_ai_provider_malformed_json_fallback()
    print("\nALL EXTRACTION TESTS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    asyncio.run(main())
