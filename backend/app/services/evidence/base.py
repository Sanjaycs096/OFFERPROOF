import re
import ipaddress
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional, Dict, Any
from urllib.parse import urlparse

from app.schemas.extraction import ExtractedInformation
from app.schemas.evidence import EvidenceItem, TechnicalObservation

# Standard 2-part ccTLDs to extract registrable domain correctly
TWO_PART_TLDS = {
    "co.uk", "org.uk", "gov.uk", "ac.uk", "me.uk",
    "co.in", "net.in", "org.in", "gen.in", "firm.in", "ind.in", "ac.in", "edu.in", "res.in", "gov.in",
    "com.au", "net.au", "org.au", "edu.au", "gov.au",
    "co.nz", "net.nz", "org.nz",
    "co.za", "org.za", "net.za",
    "com.br", "net.br", "org.br",
    "com.mx", "org.mx",
    "co.jp", "ne.jp", "or.jp",
    "com.sg", "edu.sg",
}


def normalize_hostname(raw_url_or_domain: Optional[str]) -> Optional[str]:
    """
    Extracts and normalizes a clean, lowercased hostname from a URL, email, or domain string.
    Strips protocol, paths, ports, and trailing dots.
    """
    if not raw_url_or_domain or not raw_url_or_domain.strip():
        return None

    cleaned = raw_url_or_domain.strip().lower()

    # If email address passed, extract domain part
    if "@" in cleaned:
        cleaned = cleaned.split("@")[-1].strip()

    # If scheme missing, prepend https:// for urlparse
    if "://" not in cleaned:
        cleaned = "https://" + cleaned

    try:
        parsed = urlparse(cleaned)
        hostname = parsed.hostname
        if not hostname:
            return None
        # Remove trailing dot if present
        hostname = hostname.rstrip(".")
        return hostname if hostname else None
    except Exception:
        return None


def is_safe_public_hostname(hostname: Optional[str]) -> bool:
    """
    Strict security check:
    Rejects localhost, private IP ranges (RFC 1918), link-local, loopback,
    metadata endpoints (169.254.169.254), and invalid domain formats.
    """
    if not hostname:
        return False

    hostname = hostname.lower().strip()

    # 1. Reject localhost and reserved names
    if hostname in ("localhost", "localhost.localdomain", "broadcasthost", "local"):
        return False
    if hostname.endswith((".local", ".internal", ".arpa", ".test", ".example", ".invalid", ".localhost")):
        # Note: .example is reserved for documentation/testing per RFC 2606
        # Allow .example only for mock testing, but reject strictly internal network suffixes
        if hostname.endswith((".local", ".internal", ".arpa", ".localhost")):
            return False

    # 2. Check if hostname is an IP address
    try:
        ip = ipaddress.ip_address(hostname)
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_multicast or ip.is_reserved or ip.is_unspecified:
            return False
        # Specific check for AWS/cloud metadata address
        if str(ip) == "169.254.169.254":
            return False
        return True
    except ValueError:
        # Not an IP address, proceed with domain name validation
        pass

    # 3. Domain format validation (RFC 1035)
    # Must contain at least one dot (e.g. domain.tld)
    if "." not in hostname:
        return False

    # Disallow invalid characters
    if not re.match(r"^[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?(\.[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?)+$", hostname):
        return False

    return True


def extract_registrable_domain(hostname: Optional[str]) -> Optional[str]:
    """
    Extracts the root registrable domain (e.g. careers.apex.co.uk -> apex.co.uk, sub.example.com -> example.com).
    """
    if not hostname:
        return None

    norm = normalize_hostname(hostname)
    if not norm:
        return None

    # Check if raw IP
    try:
        ipaddress.ip_address(norm)
        return norm
    except ValueError:
        pass

    parts = norm.split(".")
    if len(parts) <= 2:
        return norm

    # Check for known 2-part ccTLDs
    last_two = f"{parts[-2]}.{parts[-1]}"
    if last_two in TWO_PART_TLDS and len(parts) >= 3:
        return f"{parts[-3]}.{parts[-2]}.{parts[-1]}"

    return f"{parts[-2]}.{parts[-1]}"


class VerificationContext:
    """Carries opportunity information, extracted entities, and shared ID generators."""

    def __init__(
        self,
        extracted_information: ExtractedInformation,
        application_url: Optional[str] = None,
    ):
        self.info = extracted_information
        self.application_url = application_url
        self._evidence_counter = 1
        self._observation_counter = 1

        # Resolve primary and related domains
        self.website_hostname = normalize_hostname(self.info.organisation.website)
        self.app_hostname = normalize_hostname(application_url or self.info.application.application_url)
        self.recruiter_email_domain = normalize_hostname(self.info.recruiter.email)

        # Primary target domain for domain/DNS inspection
        self.primary_domain = (
            extract_registrable_domain(self.website_hostname)
            or extract_registrable_domain(self.app_hostname)
            or None
        )

        self.primary_hostname = self.website_hostname or self.app_hostname or None

    def next_evidence_id(self) -> str:
        eid = f"EVD-{self._evidence_counter:03d}"
        self._evidence_counter += 1
        return eid

    def next_observation_id(self) -> str:
        oid = f"OBS-{self._observation_counter:03d}"
        self._observation_counter += 1
        return oid


class BaseEvidenceProvider(ABC):
    """Abstract base class for modular evidence providers."""

    @property
    @abstractmethod
    def provider_name(self) -> str:
        pass

    @abstractmethod
    async def collect(
        self, context: VerificationContext
    ) -> Tuple[List[EvidenceItem], List[TechnicalObservation]]:
        """Collects evidence items and technical observations."""
        pass

