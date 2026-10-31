import re
from typing import List, Dict, Any, Optional, Tuple
from app.schemas.extraction import (
    OrganisationInfo,
    OpportunityInfo,
    FinancialDetails,
    RecruiterInfo,
    ApplicationInfo,
    ExtractedInformation,
    ClaimItem,
    SuspiciousIndicator,
    ExtractionSummary,
    ExtractionResponse,
)
from app.schemas.ingestion import UrlMetadata
from app.services.ingestion_service import parse_url_metadata


class FallbackExtractor:
    """
    Deterministic rule-based extractor for Phase 2.
    Extracts structured entities, payment amounts, emails, URLs,
    suspicious language indicators, and individual claims from raw text.
    """

    # Suspicious indicator patterns
    INDICATOR_PATTERNS = [
        (
            "guaranteed_selection",
            r"(?i)\b(guaranteed\s+(?:selection|placement|job|internship|admission)|100%\s*(?:job\s*)?placement|direct\s+selection(?:\s+without\s+interview)?)\b",
            "Claims guaranteed selection, bypassing normal merit or interview evaluation.",
        ),
        (
            "registration_fee_request",
            r"(?i)\b(?:pay|deposit|transfer|send)?\s*(?:a\s+)?(?:registration|training|processing|material|onboarding|security)\s+fee\b|\bpay\s+[₹$€£\d,]+\s*(?:as|for)?\s*(?:a\s+)?(?:registration|training|processing|security)?\s*fee\b",
            "Requests candidate payment for registration, training, or onboarding.",
        ),
        (
            "urgent_payment_demand",
            r"(?i)\b(pay\s+(?:immediately|urgently|today|within\s+\d+\s+hours)|urgent\s+payment|last\s+chance\s+to\s+pay)\b",
            "Creates artificial pressure for rapid financial disbursement.",
        ),
        (
            "unauthenticated_channel",
            r"(?i)\b(contact\s+(?:via|on)\s+telegram|telegram(?:\s+username|\s+channel)?\s*:\s*@?[a-zA-Z0-9_]+|whatsapp\s+(?:only|interview))\b",
            "Directs official corporate hiring through informal or anonymous messaging channels.",
        ),
        (
            "sensitive_info_request",
            r"(?i)\b(?:provide|send|submit)\s+(?:your\s+)?(?:bank\s+account|otp|password|debit\s+card|credit\s+card|pin\s+code|ssn)\b",
            "Solicits sensitive financial or identity credentials prematurely.",
        ),
        (
            "artificial_urgency",
            r"(?i)\b(limited\s+seats\s+left|offer\s+expires\s+in\s+\d+\s+hours|immediate\s+joining\s+mandatory|first\s+\d+\s+candidates\s+only)\b",
            "Utilizes high-pressure urgency tactics commonly associated with recruitment scams.",
        ),
    ]

    def extract(
        self,
        text: str,
        source_type: str = "text",
        application_url: Optional[str] = None,
    ) -> ExtractionResponse:
        claims: List[ClaimItem] = []
        indicators: List[SuspiciousIndicator] = []
        claim_counter = 1

        def next_claim_id():
            nonlocal claim_counter
            cid = f"CLM-{claim_counter:03d}"
            claim_counter += 1
            return cid

        # 1. Recruiter Information
        recruiter_emails = re.findall(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", text
        )
        recruiter_email = recruiter_emails[0] if recruiter_emails else None

        recruiter_phones = re.findall(
            r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b", text
        )
        recruiter_phone = recruiter_phones[0] if recruiter_phones else None

        recruiter_handles = re.findall(
            r"(?i)(?:telegram|telegram\s+handle|skype|whatsapp)\s*[:@-]?\s*([@\w\d_]+)", text
        )
        contact_info = recruiter_handles[0] if recruiter_handles else None

        recruiter_name_match = re.search(
            r"(?i)(?:recruiter|hr(?:\s+manager)?|contact(?:\s+person)?|regards,?|sincerely,?)\s*[:\-]?\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,2})",
            text,
        )
        recruiter_name = recruiter_name_match.group(1).strip() if recruiter_name_match else None

        recruiter = RecruiterInfo(
            name=recruiter_name,
            email=recruiter_email,
            phone=recruiter_phone,
            contact_info=contact_info,
        )

        if recruiter_email:
            pos = self._find_position(text, recruiter_email)
            claims.append(
                ClaimItem(
                    claim_id=next_claim_id(),
                    claim_text=f"Recruiter contact email is stated as {recruiter_email}.",
                    claim_category="recruiter",
                    extracted_value=recruiter_email,
                    source_text=self._get_context_span(text, recruiter_email),
                    source_position=pos,
                    confidence=0.95,
                    verification_status="not_checked",
                )
            )

        # 2. Organisation Information
        org_match = re.search(
            r"(?i)\b(?:at|by|with|from)\s+([A-Z][a-zA-Z0-9\s&]+?(?:Technologies|Technology|Tech|LLC|Inc|Corp|Corporation|Ltd|Limited|Solutions|Labs|Systems|University|Institute|Foundation|Enterprises|Group|Studio))\b",
            text,
        )
        if not org_match:
            org_match = re.search(
                r"(?i)\b(?:at|by|from)\s+([A-Z][A-Za-z0-9]+(?:\s+[A-Z][A-Za-z0-9]+){1,3})\b",
                text,
            )

        org_name = org_match.group(1).strip() if org_match else None

        # Clean trailing punctuation from org_name
        if org_name:
            org_name = re.sub(r"[.,;:]$", "", org_name)

        org_website_match = re.search(
            r"(?i)\b(?:visit|website|portal)?\s*:?\s*(https?://[^\s<>\"']+|www\.[^\s<>\"']+)\b",
            text,
        )
        org_website = org_website_match.group(1) if org_website_match else None

        org_type = None
        if org_name:
            if re.search(r"(?i)University|College|Institute|School", org_name):
                org_type = "educational_institution"
            elif re.search(r"(?i)Foundation|Trust|Charity|NGO", org_name):
                org_type = "non_profit"
            else:
                org_type = "corporate_entity"

        organisation = OrganisationInfo(
            name=org_name,
            website=org_website,
            organisation_type=org_type,
        )

        if org_name:
            pos = self._find_position(text, org_name)
            claims.append(
                ClaimItem(
                    claim_id=next_claim_id(),
                    claim_text=f"Organisation claims to be {org_name}.",
                    claim_category="organisation",
                    extracted_value=org_name,
                    source_text=self._get_context_span(text, org_name),
                    source_position=pos,
                    confidence=0.90,
                    verification_status="not_checked",
                )
            )

        # 3. Opportunity Information
        role_match = re.search(
            r"(?i)\b(?:selected for|offer for|opportunity as|position of|role of|hiring for|seeking a|seeking an)\s+(?:a\s+|an\s+)?([A-Za-z\s]+?(?:Internship|Intern|Developer|Engineer|Analyst|Scientist|Specialist|Fellowship|Scholarship|Associate|Consultant|Manager|Executive|Designer))\b",
            text,
        )
        if not role_match:
            role_match = re.search(
                r"(?i)\b([A-Za-z\s]{3,35}?(?:Internship|Intern|Fellowship|Scholarship))\b",
                text,
            )

        opp_role = role_match.group(1).strip() if role_match else None
        if opp_role:
            opp_role = re.sub(r"\s+", " ", opp_role)

        opp_category = "job"
        if opp_role and re.search(r"(?i)Intern|Internship", opp_role):
            opp_category = "internship"
        elif opp_role and re.search(r"(?i)Scholarship|Fellowship|Grant", opp_role):
            opp_category = "scholarship"
        elif re.search(r"(?i)Scholarship|Fellowship", text):
            opp_category = "scholarship"
        elif re.search(r"(?i)Intern|Internship", text):
            opp_category = "internship"

        # Work arrangement
        arrangement_match = re.search(
            r"(?i)\b(remote|work from home|hybrid|on-site|onsite|in-office)\b", text
        )
        work_arrangement = (
            arrangement_match.group(1).lower().replace("work from home", "remote")
            if arrangement_match
            else None
        )

        # Deadline
        deadline_match = re.search(
            r"(?i)\b(?:before|by|deadline(?:\s*is)?|last date(?:\s*is)?|apply before)\s+([A-Za-z0-9\s,]+?(?:\d{4}|\d{1,2}(?:st|nd|rd|th)?|\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}))\b",
            text,
        )
        application_deadline = (
            deadline_match.group(1).strip() if deadline_match else None
        )

        # Duration
        duration_match = re.search(
            r"(?i)\b(\d+\s*(?:weeks?|months?|years?))\s+(?:duration|program|internship|contract)\b|\b(?:duration\s*:\s*)(\d+\s*(?:weeks?|months?|years?))\b",
            text,
        )
        duration = None
        if duration_match:
            duration = (duration_match.group(1) or duration_match.group(2)).strip()

        opportunity = OpportunityInfo(
            title=opp_role or "Opportunity Listing",
            category=opp_category,
            role=opp_role,
            required_qualifications=[],
            required_skills=[],
            work_arrangement=work_arrangement,
            location="Remote" if work_arrangement == "remote" else None,
            duration=duration,
            application_deadline=application_deadline,
        )

        if opp_role:
            pos = self._find_position(text, opp_role)
            claims.append(
                ClaimItem(
                    claim_id=next_claim_id(),
                    claim_text=f"Organisation claims to offer a {opp_role}.",
                    claim_category="opportunity",
                    extracted_value=opp_role,
                    source_text=self._get_context_span(text, opp_role),
                    source_position=pos,
                    confidence=0.92,
                    verification_status="not_checked",
                )
            )

        if application_deadline:
            pos = self._find_position(text, application_deadline)
            claims.append(
                ClaimItem(
                    claim_id=next_claim_id(),
                    claim_text=f"Application has a stated deadline of {application_deadline}.",
                    claim_category="deadline",
                    extracted_value=application_deadline,
                    source_text=self._get_context_span(text, application_deadline),
                    source_position=pos,
                    confidence=0.88,
                    verification_status="not_checked",
                )
            )

        # 4. Financial Details
        stipend_val = None
        salary_val = None
        reg_fee_val = None
        other_fees: List[str] = []

        # Find stipend / salary
        compensation_matches = re.finditer(
            r"(?i)\b(?:earn|stipend|salary|compensation|package|offering)\s*(?:is|of|up to)?\s*:?\s*([₹$€£]\s*[\d,]+(?:\s*(?:per month|\/month|pm|per annum|\/year|pa|\/hr))?|[\d,]+\s*(?:INR|USD|EUR|GBP|LPA))\b",
            text,
        )
        for m in compensation_matches:
            val = m.group(1).strip()
            span_text = text[max(0, m.start() - 15) : min(len(text), m.end() + 15)].lower()
            if "fee" not in span_text and "pay" not in span_text:
                if opp_category == "internship":
                    stipend_val = val
                else:
                    salary_val = val
                break

        # If no compensation match found by prefix, check direct amount patterns with "per month"
        if not stipend_val and not salary_val:
            direct_pay = re.search(
                r"(?i)([₹$€£]\s*[\d,]+(?:\s*(?:per month|\/month|pm|per year|\/year|pa|\/hr)))\b",
                text,
            )
            if direct_pay:
                val = direct_pay.group(1).strip()
                if opp_category == "internship":
                    stipend_val = val
                else:
                    salary_val = val

        # Find registration / processing fee
        fee_match = re.search(
            r"(?i)\bpay\s+([₹$€£]\s*[\d,]+|[\d,]+\s*(?:INR|USD|EUR|GBP))\s*(?:as|for)?\s*(?:a\s+)?(?:registration|processing|training|onboarding|security)?\s*fee\b",
            text,
        )
        if not fee_match:
            fee_match = re.search(
                r"(?i)\b(?:registration|processing|training|onboarding|security)\s+fee(?:\s*is|\s*of)?\s*:?\s*([₹$€£]\s*[\d,]+|[\d,]+\s*(?:INR|USD|EUR|GBP))\b",
                text,
            )

        if fee_match:
            reg_fee_val = fee_match.group(1).strip()
            other_fees.append(f"Registration fee of {reg_fee_val}")

        financial = FinancialDetails(
            salary=salary_val,
            stipend=stipend_val,
            registration_fees=reg_fee_val,
            training_fees=None,
            processing_fees=None,
            other_payment_requests=other_fees if not reg_fee_val else [],
        )

        if stipend_val:
            pos = self._find_position(text, stipend_val)
            claims.append(
                ClaimItem(
                    claim_id=next_claim_id(),
                    claim_text=f"Advertised monthly stipend is {stipend_val}.",
                    claim_category="financial",
                    extracted_value=stipend_val,
                    source_text=self._get_context_span(text, stipend_val),
                    source_position=pos,
                    confidence=0.91,
                    verification_status="not_checked",
                )
            )

        if salary_val:
            pos = self._find_position(text, salary_val)
            claims.append(
                ClaimItem(
                    claim_id=next_claim_id(),
                    claim_text=f"Advertised compensation is {salary_val}.",
                    claim_category="financial",
                    extracted_value=salary_val,
                    source_text=self._get_context_span(text, salary_val),
                    source_position=pos,
                    confidence=0.90,
                    verification_status="not_checked",
                )
            )

        if reg_fee_val:
            pos = self._find_position(text, reg_fee_val)
            claims.append(
                ClaimItem(
                    claim_id=next_claim_id(),
                    claim_text=f"Applicant is asked to pay {reg_fee_val} as a registration fee.",
                    claim_category="financial",
                    extracted_value=reg_fee_val,
                    source_text=self._get_context_span(text, reg_fee_val),
                    source_position=pos,
                    confidence=0.95,
                    verification_status="not_checked",
                )
            )

        # 5. Suspicious Indicators
        for ind_type, pattern, description in self.INDICATOR_PATTERNS:
            matches = list(re.finditer(pattern, text))
            for m in matches:
                statement = m.group(0).strip()
                quote = self._get_context_span(text, statement)
                indicators.append(
                    SuspiciousIndicator(
                        indicator_type=ind_type,
                        statement=statement,
                        description=description,
                        source_quote=quote,
                    )
                )

                # Avoid duplicate claim if already captured in financial claims
                if ind_type == "registration_fee_request" and reg_fee_val:
                    continue

                # Add corresponding claim for suspicious statement
                pos = {"start": m.start(), "end": m.end()}
                claim_desc = f"Message states: '{statement}'."
                if ind_type == "guaranteed_selection":
                    claim_desc = "Message claims guaranteed selection."
                elif ind_type == "urgent_payment_demand":
                    claim_desc = "Message demands urgent payment."

                claims.append(
                    ClaimItem(
                        claim_id=next_claim_id(),
                        claim_text=claim_desc,
                        claim_category="suspicious_indicator",
                        extracted_value=statement,
                        source_text=quote,
                        source_position=pos,
                        confidence=0.89,
                        verification_status="not_checked",
                    )
                )

        # 6. Application Info
        raw_urls = re.findall(r"https?://[^\s<>\"']+|www\.[^\s<>\"']+", text)
        direct_app_url = application_url or (raw_urls[0] if raw_urls else None)

        application = ApplicationInfo(
            application_url=direct_app_url,
            application_email=recruiter_email,
            application_instructions="Submit details via application channel."
            if (direct_app_url or recruiter_email)
            else None,
        )

        if application_url:
            claims.append(
                ClaimItem(
                    claim_id=next_claim_id(),
                    claim_text=f"Application portal URL is referenced as {application_url}.",
                    claim_category="application",
                    extracted_value=application_url,
                    source_text=application_url,
                    source_position=None,
                    confidence=0.95,
                    verification_status="not_checked",
                )
            )

        # 7. Summary
        total_entities = sum(
            [
                bool(org_name),
                bool(opp_role),
                bool(stipend_val or salary_val),
                bool(reg_fee_val),
                bool(recruiter_email),
                bool(application_deadline),
                bool(work_arrangement),
            ]
        )

        extracted_info = ExtractedInformation(
            organisation=organisation,
            opportunity=opportunity,
            financial_details=financial,
            recruiter=recruiter,
            application=application,
        )

        summary = ExtractionSummary(
            total_claims=len(claims),
            total_entities=total_entities,
            detected_indicators=len(indicators),
        )

        url_meta = parse_url_metadata(application_url)

        return ExtractionResponse(
            success=True,
            extraction_mode="rule_based",
            source_type=source_type,
            extracted_information=extracted_info,
            claims=claims,
            suspicious_indicators=indicators,
            extraction_summary=summary,
            url_metadata=url_meta,
            errors=None,
        )

    def _find_position(self, full_text: str, target: str) -> Optional[Dict[str, int]]:
        idx = full_text.find(target)
        if idx != -1:
            return {"start": idx, "end": idx + len(target)}
        return None

    def _get_context_span(self, full_text: str, target: str, window: int = 50) -> str:
        idx = full_text.find(target)
        if idx == -1:
            return target
        start = max(0, idx - window)
        end = min(len(full_text), idx + len(target) + window)
        snippet = full_text[start:end].strip()
        if start > 0:
            snippet = "..." + snippet
        if end < len(full_text):
            snippet = snippet + "..."
        return snippet


fallback_extractor = FallbackExtractor()
