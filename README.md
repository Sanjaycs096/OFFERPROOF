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

## Current Status: Phase 2 — Ingestion & Claim Extraction

Phase 2 introduces the ingestion and claim extraction pipeline, converting unstructured opportunity text and PDF documents into structured, machine-readable claims:
- **Multi-Source Ingestion:** Pasted text, text-based PDF documents (via in-memory PyMuPDF), and SSRF-safe URL reference extraction.
- **Claim Extraction Engine:** Dissects offers into verifiable, atomic claims (organisation, opportunity, financial, deadline, recruiter) with `verification_status="not_checked"`.
- **Modular AI & Fallback Integration:** Pluggable AI extraction (Google Gemini / OpenAI-compatible models) backed by a deterministic, zero-dependency pattern recognition fallback.
- **Suspicious Language Observation:** Extracts linguistic red flags (guaranteed selection, urgent payment demands, unauthenticated channels) as observational evidence without concluding fraud.
- **Dynamic Frontend Dashboard:** Interactive extraction inspector with claim cards, entity breakdown tabs, confidence meters, and JSON export.

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
│   │   │   ├── ExtractionResults.jsx# Claim scorecard, entity cards & JSON inspector
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
│   │   │   └── ingestion.py         # Ingestion & extraction endpoints (/api/v1/...)
│   │   ├── schemas/
│   │   │   ├── __init__.py          # Schema exports
│   │   │   ├── health.py            # Pydantic models for health and root responses
│   │   │   ├── ingestion.py         # Ingestion request and response models
│   │   │   └── extraction.py        # Pydantic models for claims and entities
│   │   ├── services/
│   │   │   ├── __init__.py          # Service exports
│   │   │   ├── health_service.py    # Service logic for health inspection
│   │   │   ├── pdf_service.py       # In-memory PyMuPDF validation and text extraction
│   │   │   ├── ingestion_service.py # Text sanitization and SSRF-safe URL parsing
│   │   │   ├── fallback_extractor.py# Deterministic regex and pattern-based extractor
│   │   │   ├── ai_service.py        # Modular AI provider abstraction (Gemini / OpenAI)
│   │   │   └── extraction_service.py# Extraction pipeline coordinator
│   │   ├── __init__.py              # Backend package metadata
│   │   └── main.py                  # FastAPI application entry point, CORS, and root GET /
│   ├── tests/
│   │   ├── test_api.py              # Automated API and CORS tests
│   │   ├── test_pdf.py              # PyMuPDF extraction, size and page limit tests
│   │   ├── test_extraction.py       # Entity, claim, and AI fallback test suite
│   │   ├── test_ingestion.py        # Multipart PDF and text ingestion endpoint tests
│   │   └── test_live_server.py      # Live Uvicorn server socket test
│   ├── requirements.txt             # Backend Python dependencies
│   └── .env.example                 # Backend environment template
│
├── .gitignore                       # Multi-stack Git ignore rules
├── LICENSE                          # MIT License
└── README.md                        # Project documentation
```

---

## Phase 2 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Basic API information and documentation links. |
| `GET` | `/health` | Service health status and environment metadata. |
| `GET` | `/api/v1/health` | Versioned health reporting ingestion capabilities and active AI provider. |
| `POST` | `/api/v1/ingest/text` | Ingests pasted opportunity text, returns sanitized text and parsed URL hostname. |
| `POST` | `/api/v1/ingest/pdf` | Uploads a text-based PDF (`multipart/form-data`), extracts text in-memory via PyMuPDF. |
| `POST` | `/api/v1/extract` | Extracts structured entities, atomic claims, and suspicious language indicators. |

Interactive API documentation is available at `http://localhost:8000/docs` (Swagger UI) and `http://localhost:8000/redoc`.

---

## AI Provider Configuration

OFFERPROOF includes a pluggable AI extraction architecture with automatic deterministic fallback.

In `backend/.env`:

```ini
# Provider options: "gemini", "openai", "none" (defaults to "none" if keys omitted)
AI_PROVIDER=gemini
AI_REQUEST_TIMEOUT_SECONDS=25.0

# Option A: Google Gemini
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-flash

# Option B: OpenAI-Compatible (OpenAI, Groq, Ollama, DeepSeek)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o-mini
```

> **Security Note:** User submissions are encapsulated within `<untrusted_opportunity_text>` delimiters to prevent prompt injection. If an AI provider is unconfigured, times out, or returns invalid schema, the system automatically falls back to `fallback_extractor.py`, marking `extraction_mode="rule_based"`.

---

## Example Extraction Response (`POST /api/v1/extract`)

```json
{
  "success": true,
  "extraction_mode": "rule_based",
  "source_type": "text",
  "extracted_information": {
    "organisation": {
      "name": "ABC Technologies",
      "website": null,
      "organisation_type": "corporate_entity"
    },
    "opportunity": {
      "title": "Data Science Internship",
      "category": "internship",
      "role": "Data Science Internship",
      "required_qualifications": [],
      "required_skills": [],
      "work_arrangement": null,
      "location": null,
      "duration": null,
      "application_deadline": "October 31"
    },
    "financial_details": {
      "salary": null,
      "stipend": "₹45,000 per month",
      "registration_fees": "₹1,500",
      "training_fees": null,
      "processing_fees": null,
      "other_payment_requests": []
    },
    "recruiter": {
      "name": null,
      "email": null,
      "phone": null,
      "contact_info": null
    },
    "application": {
      "application_url": "https://abctech.example.com/apply",
      "application_email": null,
      "application_instructions": "Submit details via application channel."
    }
  },
  "claims": [
    {
      "claim_id": "CLM-001",
      "claim_text": "Organisation claims to be ABC Technologies.",
      "claim_category": "organisation",
      "extracted_value": "ABC Technologies",
      "source_text": "...selected for a Data Science Internship at ABC Technologies. Earn ₹45,000 per month...",
      "source_position": { "start": 62, "end": 78 },
      "confidence": 0.9,
      "verification_status": "not_checked"
    },
    {
      "claim_id": "CLM-002",
      "claim_text": "Organisation claims to offer a Data Science Internship.",
      "claim_category": "opportunity",
      "extracted_value": "Data Science Internship",
      "source_text": "...Congratulations! You have been selected for a Data Science Internship at ABC Technologies...",
      "source_position": { "start": 36, "end": 59 },
      "confidence": 0.92,
      "verification_status": "not_checked"
    },
    {
      "claim_id": "CLM-003",
      "claim_text": "Application has a stated deadline of October 31.",
      "claim_category": "deadline",
      "extracted_value": "October 31",
      "source_text": "...Pay ₹1,500 as a registration fee before October 31. Guaranteed selection...",
      "source_position": { "start": 139, "end": 149 },
      "confidence": 0.88,
      "verification_status": "not_checked"
    },
    {
      "claim_id": "CLM-004",
      "claim_text": "Advertised monthly stipend is ₹45,000 per month.",
      "claim_category": "financial",
      "extracted_value": "₹45,000 per month",
      "source_text": "...at ABC Technologies. Earn ₹45,000 per month. Pay ₹1,500 as a registration fee...",
      "source_position": { "start": 85, "end": 102 },
      "confidence": 0.91,
      "verification_status": "not_checked"
    },
    {
      "claim_id": "CLM-005",
      "claim_text": "Applicant is asked to pay ₹1,500 as a registration fee.",
      "claim_category": "financial",
      "extracted_value": "₹1,500",
      "source_text": "...Earn ₹45,000 per month. Pay ₹1,500 as a registration fee before October 31...",
      "source_position": { "start": 108, "end": 114 },
      "confidence": 0.95,
      "verification_status": "not_checked"
    },
    {
      "claim_id": "CLM-006",
      "claim_text": "Message claims guaranteed selection.",
      "claim_category": "suspicious_indicator",
      "extracted_value": "Guaranteed selection",
      "source_text": "...registration fee before October 31. Guaranteed selection.",
      "source_position": { "start": 151, "end": 171 },
      "confidence": 0.89,
      "verification_status": "not_checked"
    }
  ],
  "suspicious_indicators": [
    {
      "indicator_type": "guaranteed_selection",
      "statement": "Guaranteed selection",
      "description": "Claims guaranteed selection, bypassing normal merit or interview evaluation.",
      "source_quote": "...registration fee before October 31. Guaranteed selection."
    },
    {
      "indicator_type": "registration_fee_request",
      "statement": "Pay ₹1,500 as a registration fee",
      "description": "Requests candidate payment for registration, training, or onboarding.",
      "source_quote": "...Earn ₹45,000 per month. Pay ₹1,500 as a registration fee before October 31..."
    }
  ],
  "extraction_summary": {
    "total_claims": 6,
    "total_entities": 4,
    "detected_indicators": 2
  },
  "url_metadata": {
    "submitted_url": "https://abctech.example.com/apply",
    "hostname": "abctech.example.com",
    "scheme": "https",
    "path": "/apply"
  },
  "errors": null
}
```

---

## Installation & Setup Instructions

### Prerequisites
- [Node.js](https://nodejs.org/) (v18.0.0 or higher recommended, tested on v24.12.0)
- [Python](https://www.python.org/) (v3.10 or higher recommended)
- [Git](https://git-scm.com/)

---

### 1. Clone the Repository

```bash
git clone https://github.com/Sanjaycs096/OFFERPROOF.git
cd OFFERPROOF
```

---

### 2. Backend Setup

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create and activate a Python virtual environment:**
   - **On Windows (PowerShell):**
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
   - **On macOS / Linux:**
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Install backend dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```

5. **Start the FastAPI backend server:**
   ```bash
   uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
   ```

---

### 3. Frontend Setup

1. **Open a new terminal window and navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install frontend npm dependencies:**
   ```bash
   npm install
   ```

3. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```

4. **Start the Vite development server:**
   ```bash
   npm run dev
   ```

5. **Access the application:**
   - Open your browser at `http://localhost:5173`.
   - The top navigation bar displays a live indicator: **`API Online (<ms>ms)`**.
   - Paste job or offer text, or drag & drop a PDF document to extract verifiable claims.

---

### 4. Running Backend Tests

Execute all Phase 2 automated test suites:

```bash
# PDF Ingestion & Limits (Empty PDF, file size, max pages, signature)
.\backend\.venv\Scripts\python.exe backend\tests\test_pdf.py

# Claim Extraction & Fallback Engine
.\backend\.venv\Scripts\python.exe backend\tests\test_extraction.py

# Ingestion API Endpoints (Multipart PDF upload, text ingestion, extraction)
.\backend\.venv\Scripts\python.exe backend\tests\test_ingestion.py

# Live HTTP Server Socket Test
.\backend\.venv\Scripts\python.exe backend\tests\test_live_server.py
```

---

## Current Implementation Limitations (Phase 2)

- **Text-Based PDFs Only:** Scanned documents or images inside PDFs require OCR capabilities which are scheduled for future enhancements; empty or image-only PDFs are detected and rejected with informative guidance.
- **SSRF Safety:** User-submitted URLs are parsed structurally (hostname, scheme, path) for reference; automated external URL retrieval is disabled to protect against SSRF and unsafe external requests.
- **No Independent Verification or Fraud Scoring:** All claims extracted in Phase 2 are strictly marked `verification_status="not_checked"`. Independent registry checks and risk scoring will be implemented in subsequent phases.

---

## Future Development Roadmap

- [x] **Phase 1: Project Foundation**
  - Establish full-stack repository structure.
  - Configure modern React + Vite frontend and asynchronous FastAPI backend.
  - Implement bidirectional health check and CORS integration.

- [x] **Phase 2: Ingestion & Claim Extraction (Current)**
  - Multi-source ingestion: raw text, text-based PDF parsing via in-memory PyMuPDF, and SSRF-safe URL references.
  - Atomic claim extraction engine isolating verifiable claims (`verification_status="not_checked"`).
  - Pluggable AI extraction architecture with deterministic rule-based fallback.
  - Suspicious language indicator extraction without concluding fraud.
  - Interactive claim card dashboard and JSON export.

- [ ] **Phase 3: Multi-Source Evidence Cross-Referencing**
  - Corporate registry corroboration (SEC EDGAR, UK Companies House, OpenCorporates).
  - Domain WHOIS & DNS MX/SPF/DKIM verification for recruiter email authenticity.
  - Automated crawling of corporate careers portals to verify genuine requisition IDs.

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
