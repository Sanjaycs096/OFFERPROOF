import logging
from typing import Optional, List
from app.schemas.extraction import (
    ExtractionRequest,
    ExtractionResponse,
    ExtractedInformation,
    ClaimItem,
    SuspiciousIndicator,
    ExtractionSummary,
)
from app.services.ai_service import get_ai_provider, BaseAIProvider
from app.services.fallback_extractor import fallback_extractor
from app.services.ingestion_service import parse_url_metadata

logger = logging.getLogger(__name__)


class ExtractionService:
    def __init__(self, ai_provider: Optional[BaseAIProvider] = None):
        self._provider = ai_provider

    @property
    def provider(self) -> BaseAIProvider:
        if self._provider is None:
            self._provider = get_ai_provider()
        return self._provider

    async def extract(self, request: ExtractionRequest) -> ExtractionResponse:
        content = request.content.strip()
        source_type = request.source_type or "text"
        application_url = request.application_url

        # Check if caller explicitly requested rule-based extraction
        if request.force_mode == "rule_based":
            return fallback_extractor.extract(
                text=content,
                source_type=source_type,
                application_url=application_url,
            )

        # Attempt AI extraction if provider is configured
        if self.provider.is_configured and request.force_mode != "rule_based":
            try:
                ai_raw = await self.provider.extract_claims_and_entities(
                    text=content, application_url=application_url
                )

                if ai_raw and isinstance(ai_raw, dict):
                    response = self._validate_and_build_ai_response(
                        ai_raw=ai_raw,
                        source_type=source_type,
                        application_url=application_url,
                    )
                    if response:
                        return response
            except Exception as e:
                logger.warning(
                    f"AI extraction encountered an error; engaging rule-based fallback: {type(e).__name__}"
                )

        # Seamlessly fallback to deterministic extractor
        fallback_resp = fallback_extractor.extract(
            text=content,
            source_type=source_type,
            application_url=application_url,
        )

        # If AI was attempted and failed, annotate errors
        if self.provider.is_configured and request.force_mode != "rule_based":
            fallback_resp.errors = [
                "AI provider did not return a valid response. Executed deterministic rule-based extraction fallback."
            ]

        return fallback_resp

    def _validate_and_build_ai_response(
        self,
        ai_raw: dict,
        source_type: str,
        application_url: Optional[str],
    ) -> Optional[ExtractionResponse]:
        """
        Validates raw AI provider dictionary through Pydantic models.
        Enforces that all verification_status values are strictly 'not_checked'.
        """
        try:
            # Check for required schema structure
            if "extracted_information" not in ai_raw and "claims" not in ai_raw:
                logger.warning("AI response missing required top-level keys ('extracted_information' or 'claims').")
                return None

            raw_info = ai_raw.get("extracted_information", {})
            if not isinstance(raw_info, dict):
                return None
            extracted_info = ExtractedInformation(**raw_info)

            # Build claims with strict 'not_checked' status
            raw_claims = ai_raw.get("claims", [])
            claims: List[ClaimItem] = []
            for i, c in enumerate(raw_claims):
                if not isinstance(c, dict):
                    continue

                cid = c.get("claim_id") or f"CLM-{i + 1:03d}"
                ctext = c.get("claim_text") or "Unspecified claim"
                ccat = c.get("claim_category") or "other"
                cval = c.get("extracted_value")
                csrc = c.get("source_text") or ctext
                conf = float(c.get("confidence", 0.90))
                conf = max(0.0, min(1.0, conf))

                claims.append(
                    ClaimItem(
                        claim_id=cid,
                        claim_text=ctext,
                        claim_category=ccat,
                        extracted_value=cval,
                        source_text=csrc,
                        source_position=c.get("source_position"),
                        confidence=conf,
                        verification_status="not_checked",
                    )
                )

            # Build suspicious indicators
            raw_indicators = ai_raw.get("suspicious_indicators", [])
            indicators: List[SuspiciousIndicator] = []
            for ind in raw_indicators:
                if not isinstance(ind, dict):
                    continue
                itype = ind.get("indicator_type") or "unspecified"
                istat = ind.get("statement") or ""
                idesc = ind.get("description") or "Suspicious language indicator noted."
                iquote = ind.get("source_quote")

                if istat:
                    indicators.append(
                        SuspiciousIndicator(
                            indicator_type=itype,
                            statement=istat,
                            description=idesc,
                            source_quote=iquote,
                        )
                    )

            # Calculate entity count
            total_entities = sum(
                [
                    bool(extracted_info.organisation.name),
                    bool(extracted_info.opportunity.role or extracted_info.opportunity.title),
                    bool(extracted_info.financial_details.stipend or extracted_info.financial_details.salary),
                    bool(extracted_info.financial_details.registration_fees),
                    bool(extracted_info.recruiter.email or extracted_info.recruiter.name),
                    bool(extracted_info.opportunity.application_deadline),
                    bool(extracted_info.opportunity.work_arrangement),
                ]
            )

            summary = ExtractionSummary(
                total_claims=len(claims),
                total_entities=total_entities,
                detected_indicators=len(indicators),
            )

            url_meta = parse_url_metadata(application_url)

            return ExtractionResponse(
                success=True,
                extraction_mode="ai",
                source_type=source_type,
                extracted_information=extracted_info,
                claims=claims,
                suspicious_indicators=indicators,
                extraction_summary=summary,
                url_metadata=url_meta,
                errors=None,
            )
        except Exception as e:
            logger.warning(f"Validation of AI response failed: {str(e)}")
            return None


extraction_service = ExtractionService()
