# OFFERPROOF

> **Don't trust the offer. Verify the evidence.**

OFFERPROOF is an AI-assisted, evidence-based opportunity verification platform designed to protect students, fresh graduates, and job seekers from deceptive employment scams, ghost jobs, and fraudulent internship or scholarship offers. Rather than relying on guesswork, OFFERPROOF systematically evaluates opportunity claims against verifiable corporate registries, domain records, and public career listings to produce transparent, auditable verification scorecards.

---

## The Problem

Recruitment and scholarship fraud is surging, particularly targeting vulnerable job seekers and early-career talent:
- **Upfront Fee Scams:** Imposters pose as reputable firms, demanding equipment fees, onboarding costs, or visa processing charges.
- **Spoofed Communication:** Scammers utilize lookalike domain names (`@company-careers-portal.com`) or consumer messaging apps (Telegram, WhatsApp) while posing as verified hiring managers.
- **Ghost Jobs & Phantom Listings:** Fake listings harvest candidate resumes, personal identifiable information (PII), or cryptocurrency wallet details.
- **Lack of Auditable Evidence:** Existing tools offer vague warnings or black-box predictions without showing the verifiable proof behind an assessment.

OFFERPROOF bridges this gap by grounding every verification assessment in external, verifiable organizational evidence.

---

## Current Status: Phase 3 — Independent Evidence Verification & Source Intelligence

Phase 3 introduces an independent evidence-verification layer that audits public technical signals associated with an opportunity, connects evidence to extracted claims, and displays an itemized evidence report:

- **Domain Intelligence (RDAP):** Registration timestamp, registrar name, domain age calculation, and newly-registered domain risk detection ($<30$ days, $30\text{--}180$ days, $>180$ days).
- **DNS-over-HTTPS (DoH) Intelligence:** Resolves active `A`, `AAAA`, `MX` (mail exchanger), `NS`, and `TXT`/`SPF` records via Cloudflare DoH with strict timeouts.
- **Recruiter Email-Domain Consistency:** Compares recruiter email domains against opportunity domains and detects public consumer webmail providers (`gmail.com`, `yahoo.com`, `outlook.com`, etc.).
- **URL & Transport Consistency:** Verifies HTTPS protocol, detects raw IP addresses in links, and checks subdomain alignment against claimed corporate websites.
- **Strict SSRF & Injection Safety:** Submitted URLs are structurally parsed only; external target websites are **never visited or scraped**.
- **Claim-to-Evidence Mapping:** Connects each extracted claim to relevant technical evidence artifacts. Factual claims that cannot be resolved through technical network evidence (such as salaries, stipends, and job openings) remain strictly marked `verification_status="not_checked"`.
- **Defensible Statuses:** Strictly avoids converting indirect technical observations into confirmed fraud verdicts.

---

## Technology Stack

### Frontend
- **Framework:** React 18
- **Build Tool:** Vite 5
- **Styling:** Tailwind CSS (Navy / Cyber Slate cybersecurity theme)
- **Icons:** Lucide React
- **Language:** JavaScript (ES Modules)

### Backend
- **Framework:** FastAPI
- **ASGI Server:** Uvicorn
- **Document Parsing:** PyMuPDF (`pymupdf`)
- **Multipart Form Uploads:** `python-multipart`
- **Data Validation & Schemas:** Pydantic v2 & Pydantic-Settings
- **HTTP Client (Async):** HTTPX
- **Environment Management:** python-dotenv
- **Language:** Python 3.10+

### DevOps & Tooling
- **Version Control:** Git & GitHub
- **Package Managers:** npm (Frontend), pip (Backend)
- **Virtual Environment:** Python venv

---

## Project Structure

```
OFFERPROOF/
├── frontend/
│   ├── public/
│   │   └── shield.svg               # Branding icon
│   ├── src/
│   │   ├── assets/                  # Static assets
│   │   ├── components/
│   │   │   ├── Navbar.jsx           # Header with real-time API health badge
│   │   │   ├── Hero.jsx             # Hero section and value propositions
│   │   │   ├── SubmissionForm.jsx   # Ingestion intake with drag & drop PDF upload
│   │   │   ├── ExtractionResults.jsx# Claims scorecard, evidence cards & JSON inspector
│   │   │   ├── HowItWorks.jsx       # 4-stage verification pipeline explanation
│   │   │   ├── Disclaimer.jsx       # Safety, privacy, and PII protection guidance
│   │   │   ├── Footer.jsx           # Project credits, repo links, and metadata
│   │   │   └── StatusBadge.jsx      # API connection & latency indicator
│   │   ├── pages/
│   │   │   └── LandingPage.jsx      # Primary dashboard landing layout
│   │   ├── services/
│   │   │   └── api.js               # Frontend API client communicating with FastAPI
│   │   ├── hooks/
│   │   │   └── useHealthCheck.js    # React hook monitoring backend status
│   │   ├── App.jsx                  # Main component root
│   │   ├── main.jsx                 # Vite application mount point
│   │   └── index.css                # Tailwind directives & global styling
│   ├── index.html                   # HTML template
│   ├── package.json                 # Frontend dependencies and scripts
│   ├── vite.config.js               # Vite bundler configuration
│   ├── tailwind.config.js           # Custom typography and cybersecurity palette
│   ├── postcss.config.js            # PostCSS configuration
│   └── .env.example                 # Frontend environment template
│
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   │   ├── __init__.py          # API route registry
│   │   │   ├── health.py            # Health check endpoint (/health)
│   │   │   ├── ingestion.py         # Ingestion endpoints (/api/v1/ingest/...)
│   │   │   └── verification.py      # Verification endpoints (/api/v1/verify, /api/v1/analyze)
│   │   ├── schemas/
│   │   │   ├── __init__.py          # Schema exports
│   │   │   ├── health.py            # Pydantic models for health and root responses
│   │   │   ├── ingestion.py         # Ingestion request and response models
│   │   │   ├── extraction.py        # Pydantic models for claims and entities
│   │   │   ├── evidence.py          # Evidence items and technical observation models
│   │   │   └── verification.py      # Verification request, summary, and response models
│   │   ├── services/
│   │   │   ├── __init__.py          # Service exports
│   │   │   ├── health_service.py    # Service logic for health inspection
│   │   │   ├── pdf_service.py       # In-memory PyMuPDF validation and text extraction
│   │   │   ├── ingestion_service.py # Text sanitization and SSRF-safe URL parsing
│   │   │   ├── fallback_extractor.py# Deterministic regex and pattern-based extractor
│   │   │   ├── ai_service.py        # Modular AI provider abstraction (Gemini / OpenAI)
│   │   │   ├── extraction_service.py# Extraction pipeline coordinator
│   │   │   ├── verification_service.py # Evidence coordinator and claim mapper
│   │   │   └── evidence/
│   │   │       ├── __init__.py      # Evidence provider exports
│   │   │       ├── base.py          # BaseEvidenceProvider, hostname normalization, SSRF safety
│   │   │       ├── domain_service.py# RDAP domain age, registrar, and status provider
│   │   │       ├── dns_service.py   # DNS-over-HTTPS (DoH) resolver (A, MX, NS, TXT)
│   │   │       ├── email_service.py # Recruiter email-domain alignment & webmail provider check
│   │   │       ├── url_service.py   # URL scheme, raw IP, and domain divergence inspection
│   │   │       └── organisation_service.py # Name-to-domain alignment & corporate registry adapter
│   │   ├── __init__.py              # Backend package metadata (v0.3.0)
│   │   └── main.py                  # FastAPI application entry point, CORS, and root GET /
│   ├── tests/
│   │   ├── test_api.py              # Automated API, CORS, and endpoint regression tests
│   │   ├── test_pdf.py              # PyMuPDF extraction, size and page limit tests
│   │   ├── test_extraction.py       # Entity, claim, and AI fallback test suite
│   │   ├── test_ingestion.py        # Multipart PDF and text ingestion endpoint tests
│   │   ├── test_verification.py     # Mocked RDAP, DoH, email, URL, and claim mapping tests
│   │   └── test_live_server.py      # Live Uvicorn server socket test across all phases
│   ├── requirements.txt             # Backend Python dependencies
│   └── .env.example                 # Backend environment template
│
├── .gitignore                       # Multi-stack Git ignore rules
├── LICENSE                          # MIT License
└── README.md                        # Project documentation
```

---

## API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Basic API information and documentation links. |
| `GET` | `/health` | Service health status and environment metadata. |
| `GET` | `/api/v1/health` | Versioned health reporting ingestion and verification engine capabilities. |
| `POST` | `/api/v1/ingest/text` | Ingests pasted opportunity text, returns sanitized text and parsed URL hostname. |
| `POST` | `/api/v1/ingest/pdf` | Uploads a text-based PDF (`multipart/form-data`), extracts text in-memory via PyMuPDF. |
| `POST` | `/api/v1/extract` | Extracts structured entities, atomic claims, and suspicious language indicators. |
| `POST` | `/api/v1/verify` | Evaluates extracted claims against independent technical evidence (RDAP, DoH, email). |
| `POST` | `/api/v1/analyze` | Convenience endpoint executing extraction and evidence verification in a single request. |

Interactive API documentation is available at `http://localhost:8000/docs` (Swagger UI) and `http://localhost:8000/redoc`.

---

## Verification Status Definitions

### Claim Verification Statuses (`verification_status`)

- `supported`: Directly confirmed by an authoritative, trustworthy external record. (Rarely applicable for technical DNS checks alone).
- `contradicted`: Directly refuted by hard contradictory evidence (e.g. non-routable address, malformed protocol).
- `inconclusive`: Technical evidence exists (e.g. domain registered recently, DNS active, free email used), but does not independently establish or refute whether the opportunity is genuine.
- `not_checked`: The claim cannot be evaluated through available technical evidence (e.g. compensation amounts, internship availability, deadlines).

### Evidence Item Statuses (`status`)

- `available`: The check successfully retrieved objective data from the source registry.
- `not_available`: The external registry returned no data, timed out, or is not yet integrated.
- `error`: The check encountered a malformed input or network failure.
- `not_applicable`: The check was skipped because the relevant input (e.g. email address or URL) was not provided.

---

## What the System Can and Cannot Verify

### What We Can Verify
- Whether a domain name exists and when it was registered via RDAP registries.
- Whether a hostname has active public DNS routing (`A`, `AAAA`, `NS`) and mail exchangers (`MX`).
- Whether the recruiter's email domain matches the opportunity website or uses a consumer webmail provider (`gmail.com`, `yahoo.com`, etc.).
- Whether an application URL uses encrypted HTTPS and whether it points to a raw IP address.
- Whether the application URL is a subdomain of the claimed organisation's domain.

### What We Cannot Verify (Strictly Retained as `not_checked`)
- **Job/Internship Availability:** DNS routing cannot verify whether an internal job requisition exists.
- **Compensation & Stipends:** Salaries cannot be confirmed through domain registration records.
- **Application Fees:** Demanded registration fees cannot be verified via public technical registries.
- **Recruiter Authorization:** An email with a matching domain name can still be spoofed without cryptographic email headers (SPF/DKIM/DMARC inspection on raw `.eml` files).
- **Legitimacy from Age:** Older domains can be compromised; new domains may belong to legitimate startups.

---

## Example Verification Response (`POST /api/v1/verify`)

```json
{
  "success": true,
  "verification_summary": {
    "total_claims": 5,
    "supported": 0,
    "contradicted": 0,
    "inconclusive": 2,
    "not_checked": 3,
    "evidence_items": 5
  },
  "claims": [
    {
      "claim_id": "CLM-001",
      "claim_text": "Organisation claims to be ABC Technologies.",
      "claim_category": "organisation",
      "extracted_value": "ABC Technologies",
      "source_text": "...selected for a Data Science Internship at ABC Technologies...",
      "confidence": 0.9,
      "verification_status": "inconclusive",
      "evidence_ids": ["EVD-001", "EVD-004", "EVD-002"],
      "verification_explanation": "Technical records exist for domain 'abctech.example.com'. However, domain existence alone does not confirm that the claimed organisation exists or that this opportunity was authorized. Authoritative corporate registries are not verified."
    },
    {
      "claim_id": "CLM-002",
      "claim_text": "Advertised monthly stipend is ₹45,000 per month.",
      "claim_category": "financial",
      "extracted_value": "₹45,000 per month",
      "source_text": "...Earn ₹45,000 per month. Pay ₹1,500 as a registration fee...",
      "confidence": 0.91,
      "verification_status": "not_checked",
      "evidence_ids": [],
      "verification_explanation": "Advertised compensation, stipends, and requested fees cannot be verified through DNS, domain registration, or technical network evidence. Retained as not_checked pending authoritative registry or employer corroboration."
    },
    {
      "claim_id": "CLM-003",
      "claim_text": "Recruiter contact email is stated as recruiter@gmail.com.",
      "claim_category": "recruiter",
      "extracted_value": "recruiter@gmail.com",
      "source_text": "...Contact recruiter@gmail.com...",
      "confidence": 0.95,
      "verification_status": "inconclusive",
      "evidence_ids": ["EVD-003"],
      "verification_explanation": "Recruiter contact utilizes a free public webmail address rather than a verified enterprise domain. This observation indicates informal communication, but cannot confirm or refute recruiter identity on technical evidence alone."
    }
  ],
  "evidence": [
    {
      "evidence_id": "EVD-001",
      "evidence_type": "domain_registration",
      "source_name": "RDAP",
      "source_url": "https://rdap.org/domain/abctech.example.com",
      "observed_value": "Registration: 2026-09-15 (46 days old)",
      "interpretation": "Domain was registered relatively recently (46 days ago). This is a notable observation requiring corroboration against the claimed organisation's founding date.",
      "retrieved_at": "2026-10-31T04:22:21Z",
      "status": "available",
      "limitations": [
        "Domain registration age does not establish organisational legitimacy.",
        "Established domains can be spoofed or compromised; new domains may represent legitimate startups."
      ]
    },
    {
      "evidence_id": "EVD-002",
      "evidence_type": "dns_records",
      "source_name": "DNS-over-HTTPS (Cloudflare DoH)",
      "source_url": "https://cloudflare-dns.com/dns-query?name=abctech.example.com",
      "observed_value": "A: 1 records (93.184.216.34); MX: 1 servers",
      "interpretation": "Hostname 'abctech.example.com' resolves actively on public DNS with 1 mail exchanger(s).",
      "retrieved_at": "2026-10-31T04:22:21Z",
      "status": "available",
      "limitations": [
        "DNS records only demonstrate internet routing configuration; they do not establish organisational legitimacy."
      ]
    },
    {
      "evidence_id": "EVD-003",
      "evidence_type": "email_domain_consistency",
      "source_name": "Email Domain Analysis",
      "source_url": null,
      "observed_value": "Recruiter email: recruiter@gmail.com [Public Consumer Webmail]",
      "interpretation": "Recruiter email utilizes a public consumer webmail provider (gmail.com).",
      "retrieved_at": "2026-10-31T04:22:21Z",
      "status": "available",
      "limitations": [
        "A different email domain is an observation, not proof of impersonation. Organisations may use outsourced recruitment agencies."
      ]
    }
  ],
  "technical_observations": [
    {
      "observation_id": "OBS-001",
      "category": "domain",
      "label": "Domain age observation",
      "finding": "recent_domain",
      "detail": "Domain was registered relatively recently (46 days ago).",
      "severity": "informational"
    },
    {
      "observation_id": "OBS-002",
      "category": "email",
      "label": "Free email provider detected",
      "finding": "free_email_provider",
      "detail": "Recruiter uses consumer webmail provider 'gmail.com' rather than an enterprise domain.",
      "severity": "notable"
    }
  ],
  "limitations": [
    "Technical checks evaluate domain, DNS, protocol, and email consistency. They cannot establish whether an opportunity or recruiter is genuine.",
    "The presence of active DNS or HTTPS indicates technical network routing, NOT organisational honesty or employment legitimacy.",
    "Authoritative government corporate registry records (e.g. SEC EDGAR, Companies House, MCA) are not queried in Phase 3; organisation incorporation remains unverified."
  ]
}
```

---

## Installation & Setup Instructions

### Prerequisites
- [Node.js](https://nodejs.org/) (v18.0.0 or higher recommended, tested on v24.12.0)
- [Python](https://www.python.org/) (v3.10 or higher recommended)
- [Git](https://git-scm.com/)

---

### Running Automated Test Suites

Execute all Phase 1, Phase 2, and Phase 3 automated test suites:

```bash
# PDF Ingestion & Limits
.\backend\.venv\Scripts\python.exe backend\tests\test_pdf.py

# Claim Extraction & Fallback Engine
.\backend\.venv\Scripts\python.exe backend\tests\test_extraction.py

# Ingestion API Endpoints (Multipart PDF upload, text ingestion)
.\backend\.venv\Scripts\python.exe backend\tests\test_ingestion.py

# Phase 3 Evidence Verification (Mocked RDAP, DoH, Email, URL consistency)
.\backend\.venv\Scripts\python.exe backend\tests\test_verification.py

# Core API Regression & CORS Preflight Tests
.\backend\.venv\Scripts\python.exe backend\tests\test_api.py

# Live HTTP Server Socket Test
.\backend\.venv\Scripts\python.exe backend\tests\test_live_server.py
```

---

## Future Development Roadmap

- [x] **Phase 1: Project Foundation**
  - Establish full-stack repository structure.
  - Configure modern React + Vite frontend and asynchronous FastAPI backend.
  - Implement bidirectional health check and CORS integration.

- [x] **Phase 2: Ingestion & Claim Extraction**
  - Multi-source ingestion: raw text, text-based PDF parsing via in-memory PyMuPDF, and SSRF-safe URL references.
  - Atomic claim extraction engine isolating verifiable claims (`verification_status="not_checked"`).
  - Pluggable AI extraction architecture with deterministic rule-based fallback.
  - Suspicious language indicator extraction without concluding fraud.

- [x] **Phase 3: Independent Evidence Verification & Source Intelligence (Current)**
  - Domain intelligence via RDAP (registration timestamp, registrar, domain age interpretation).
  - DNS intelligence via DNS-over-HTTPS (A, AAAA, MX, NS, TXT).
  - Recruiter email-domain consistency and consumer webmail detection.
  - URL transport protocol and domain divergence inspection (no external page scraping).
  - Claim-to-evidence mapper assigning `supported`, `contradicted`, `inconclusive`, and `not_checked` states with transparent explanations.
  - Verification results dashboard with itemized evidence cards, technical observations, and check limitations.

- [ ] **Phase 4: Risk Scoring & Fraud Pattern Auditing**
  - Rule-based heuristics (upfront fee requests, disposable email domains, suspicious domain age).
  - Multi-factor risk engine computing verifiable confidence and risk index.

- [ ] **Phase 5: Auditable Verification Scorecard & Candidate Guidance**
  - Exportable PDF and interactive web reports with verifiable citations and primary sources.
  - Candidate due-diligence recommendations and incident reporting integration.

---

## Safety and Privacy

OFFERPROOF operates strictly on publicly verifiable organizational claims. Users must **not** submit sensitive Personal Identifiable Information (PII) such as Social Security Numbers, banking credentials, or personal identification cards. All verification outputs are decision-support resources designed to aid in diligence, not formal legal counsel.

---

## License

This project is licensed under the [MIT License](LICENSE).
