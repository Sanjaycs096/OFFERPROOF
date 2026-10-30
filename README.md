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

## Current Status: Phase 1 — Project Foundation

Phase 1 establishes the operational core and frontend–backend integration architecture:
- Modern, cybersecurity-styled React + Vite frontend dashboard.
- Modular, asynchronous FastAPI backend architecture with health checks and CORS configuration.
- Real-time client-to-server connectivity monitoring with latency metrics.
- Structured opportunity intake interface (description, link, and future document dropzone).
- Strict separation between intake interface and future verification pipelines (zero fake verification outputs).

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
│   │   │   ├── SubmissionForm.jsx   # Opportunity intake form & Phase 1 status modal
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
│   │   │   └── health.py            # Health check endpoint (/health)
│   │   ├── schemas/
│   │   │   ├── __init__.py          # Schema exports
│   │   │   └── health.py            # Pydantic models for health and root responses
│   │   ├── services/
│   │   │   ├── __init__.py          # Service exports
│   │   │   └── health_service.py    # Service logic for health inspection
│   │   ├── __init__.py              # Backend package metadata
│   │   └── main.py                  # FastAPI application entry point, CORS, and root GET /
│   ├── tests/
│   │   ├── test_api.py              # Automated API and CORS tests
│   │   └── test_live_server.py      # Live Uvicorn server socket test
│   ├── requirements.txt             # Backend Python dependencies
│   └── .env.example                 # Backend environment template
│
├── .gitignore                       # Multi-stack Git ignore rules
├── LICENSE                          # MIT License
└── README.md                        # Project documentation
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
   *(Defaults in `.env.example` run the server on `http://localhost:8000` with CORS enabled for `http://localhost:5173`.)*

5. **Start the FastAPI backend server:**
   ```bash
   uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
   ```

6. **Verify backend endpoints:**
   - Root Info: `http://127.0.0.1:8000/`
   - Health Check: `http://127.0.0.1:8000/health`
   - Interactive Swagger Docs: `http://127.0.0.1:8000/docs`
   - ReDoc Documentation: `http://127.0.0.1:8000/redoc`

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
   *(Ensures `VITE_API_URL=http://localhost:8000` is targeted.)*

4. **Start the Vite development server:**
   ```bash
   npm run dev
   ```

5. **Access the application:**
   - Open your browser at `http://localhost:5173`.
   - The top navigation bar displays a live indicator: **`API Online (<ms>ms)`** confirming that the React application is successfully communicating with the FastAPI backend.

---

### 4. Running Backend Tests

To execute the automated API endpoint and CORS integration tests:

```bash
# From the project root with the virtual environment activated:
.\backend\.venv\Scripts\python.exe backend\tests\test_api.py
```

To run the live socket binding test:

```bash
.\backend\.venv\Scripts\python.exe backend\tests\test_live_server.py
```

---

## Future Development Roadmap

- [x] **Phase 1: Project Foundation (Current)**
  - Establish full-stack repository structure.
  - Configure modern React + Vite frontend and asynchronous FastAPI backend.
  - Implement bidirectional health check and CORS integration.
  - Build cybersecurity-styled intake UI and architectural documentation.

- [ ] **Phase 2: Ingestion & Natural Language Claim Extraction**
  - Document parser for PDF and image offer letters via OCR.
  - LLM-assisted entity recognition: extracting company identity, recruiter details, communication mediums, compensation ranges, and prerequisite fees.

- [ ] **Phase 3: Multi-Source Evidence Cross-Referencing**
  - External registry integration (SEC EDGAR, UK Companies House, OpenCorporates).
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
