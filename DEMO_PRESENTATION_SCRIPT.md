# OFFERPROOF — Hackathon Presentation & Live Demo Script

> **Tagline:** Don't trust the offer. Verify the evidence.  
> **Repository:** [https://github.com/Sanjaycs096/OFFERPROOF.git](https://github.com/Sanjaycs096/OFFERPROOF.git)  
> **Release Version:** `v0.5.0` (Production Hardened)  
> **Presenter:** Solo Full-Stack Developer & Software Architect  

---

## Table of Contents

1. [Section A — 60-Second Elevator Pitch](#section-a--60-second-elevator-pitch)
2. [Section B — 3-Minute Timed Live Demonstration Walkthrough](#section-b--3-minute-timed-live-demonstration-walkthrough)
3. [Section C — Judge-Facing Technical Architecture](#section-c--judge-facing-technical-architecture)
4. [Section D — Judge Q&A: 14 Anticipated Technical Questions & Answers](#section-d--judge-qa-14-anticipated-technical-questions--answers)
5. [Section E — Presentation Backup & Contingency Plan](#section-e--presentation-backup--contingency-plan)
6. [Section F — Final Pre-Flight Checklist](#section-f--final-pre-flight-checklist)

---

## Section A — 60-Second Elevator Pitch

*(Spoken with clear, steady pacing, natural conviction, and zero buzzwords. Time: ~55–60 seconds.)*

> "Every semester, millions of students and fresh graduates apply for jobs, internships, and scholarships. And every semester, thousands of them fall victim to sophisticated employment fraud. 
> 
> A student receives an email: *'Congratulations! You've been selected for a remote Machine Learning Internship paying ₹35,000 a month. Please transfer a ₹1,500 security deposit or registration fee to release your onboarding package and equipment.'*
> 
> When students search online, they hit a wall. Traditional scam tools either give useless black-box numbers like '87% fraud risk' without explaining anything, or they paste the text into a generic AI chatbot that hallucinates certainty and invents facts.
> 
> We built **OFFERPROOF** to solve this with a fundamental engineering rule: **Don't trust the offer. Verify the evidence.**
> 
> When an applicant submits an offer text or uploads an offer letter PDF, OFFERPROOF doesn't guess. It extracts every discrete claim, queries authoritative public infrastructure registries—RDAP domain registration records and Cloudflare DNS-over-HTTPS—evaluates recruiter email protocol consistency, and maps verifiable technical facts against unverified claims. 
> 
> Most importantly, OFFERPROOF never manufactures false certainty. It produces an explainable, evidence-backed assessment with a prioritized safety checklist and printable PDF report so candidates know exactly what to double-check before they ever pay money or surrender sensitive data."

---

## Section B — 3-Minute Timed Live Demonstration Walkthrough

This live demonstration script matches the actual, hardened OFFERPROOF UI (`v0.5.0`) and uses the built-in synthetic demonstration scenario.

```
0:00 ─── 0:30 ─── 1:00 ─── 1:45 ─── 2:15 ─── 2:45 ─── 3:00
  │        │        │        │        │        │        │
Intro    Input   Inspect   RDAP/    Safety   Print    Close
Hero     Demo    Claims    DoH      Check-   Vector   Summary
Scene    Click   Parsed    Signals  list     Report
```

---

### Segment 1: [0:00 – 0:30] Introduction & Problem Framing

- **Screen / Visual:** Browser open at `http://localhost:5173`. Hero section displays the glowing cybersecurity shield badge, the OFFERPROOF title, and the primary tagline: *"Don't trust the offer. Verify the evidence."*
- **Action:** Point cursor to the tagline and the three feature highlight pills: *Transparent Evidence*, *Zero Black-Box Scores*, and *SSRF-Safe Technical Intelligence*.
- **Spoken Script:**
  > "Hello judges. This is OFFERPROOF. Our mission is to protect early-career talent from deceptive employment and scholarship scams. 
  > 
  > Notice what our interface emphasizes right upfront: *'Don't trust the offer. Verify the evidence.'* 
  > 
  > Existing checkers try to give users a false sense of security with arbitrary risk percentages. In contrast, OFFERPROOF is built on transparent decision support: we isolate the claims made in an opportunity announcement, query independent technical ground truth, and present an auditable, evidence-backed evaluation."

---

### Segment 2: [0:30 – 1:00] Ingestion & One-Click Demo Scenario

- **Screen / Visual:** Scroll down to the intake portal showing the three intake tabs: **Paste Text**, **Upload PDF**, and **URL Reference**.
- **Action:** Click the primary pill button: **"Demo Walkthrough"** (located in the hero banner or above the intake box).
- **Spoken Script:**
  > "Let's test a realistic scenario that college students encounter daily. I'll click our one-click **'Demo Walkthrough'** button.
  > 
  > Instantly, the system loads a synthetic recruitment email from a company called 'Apex Innovations'. Notice what it claims:
  > - A remote Machine Learning Internship.
  > - A generous stipend of ₹35,000 per month.
  > - A mandatory ₹1,500 'laptop verification and processing fee' that must be paid via UPI before an urgent 48-hour deadline.
  > - And notice the contact email: `careers.apex.internship@gmail.com` paired with a website URL `http://apex-innovations-tech.biz`.
  > 
  > Now I'll click the blue primary action button: **'Analyze & Verify Opportunity'**."

---

### Segment 3: [1:00 – 2:00] Automated Analysis, Extraction & Technical Evidence

- **Screen / Visual:** Analysis spinner runs smoothly for ~1.5 seconds. The comprehensive **Opportunity Assessment Dashboard** renders, displaying the red **High Caution** banner, the Opportunity Overview card, and the Claim Breakdown.
- **Action:** 
  1. Highlight the **High caution** guidance badge at the top left.
  2. Point to the **Findings** cards with severity badges.
  3. Expand or hover over the technical evidence chips.
- **Spoken Script:**
  > "Within two seconds, the OFFERPROOF pipeline executed a full intake, extraction, technical verification, and assessment cycle.
  > 
  > First, look at the overall assessment: **High caution**. Not an opaque score, but an explainable guidance category based on explicit rules: an upfront fee was demanded and multiple technical inconsistencies were detected.
  > 
  > Look at **Finding 1**: *Mandatory Upfront Payment Demanded*. The engine identified the ₹1,500 security deposit. As our card explains: legitimate employers and scholarship programs do not require applicants to pay equipment deposits or onboarding fees.
  > 
  > Look at **Finding 2**: *Recruiter Uses Consumer Webmail*. The recruiter claims to represent an enterprise organization, yet reaches out from a public `@gmail.com` inbox rather than the company's verified email domain.
  > 
  > Look at **Finding 3**: *Domain Intelligence & Security*. We queried authoritative RDAP registries: `apex-innovations-tech.biz` was registered just days ago, operates over unencrypted HTTP, and has no enterprise mail exchange records. 
  > 
  > And critically—notice this section: **What We Verified vs What Remains Unverified**. We independently verified domain registration dates and Cloudflare DNS routing. But we explicitly mark the ₹35,000 stipend and the job vacancy as **Not Checked**. Technical DNS records can never prove whether an internal opening exists, and our software will never lie to the student by pretending otherwise."

---

### Segment 4: [2:00 – 2:40] Prioritized Safety Checklist & Printable Report

- **Screen / Visual:** Scroll down to the **Contextual Safety Recommendations** and **Prioritized Next Steps** interactive checklist.
- **Action:**
  1. Check off the first item on the candidate action checklist (*"Do not transfer the ₹1,500 fee under any circumstances"*).
  2. Click the **"Print / Save PDF"** button in the header bar.
  3. The high-resolution printable report modal appears with official branding, unique Report ID, timestamp, and methodology disclaimer.
- **Spoken Script:**
  > "Instead of leaving the candidate in anxiety, OFFERPROOF provides an immediate, prioritized safety checklist:
  > 1. *Do not transfer funds:* Never pay advance fees for equipment or onboarding.
  > 2. *Do not submit sensitive documents:* Hold back PAN, Aadhaar, Social Security numbers, or bank details.
  > 3. *Verify through official channels:* Contact the company directly using a known corporate directory or LinkedIn recruiter page.
  > 
  > If the candidate wants to discuss this offer with their university career advisor or parents, they click **'Print / Save PDF'**. 
  > 
  > OFFERPROOF renders a clean, professional due-diligence report complete with a cryptographic-grade report ID, ISO timestamp, full claim traceability, and formal disclaimers. They can print it directly or save it as a high-resolution vector PDF."

---

### Segment 5: [2:40 – 3:00] Closing & Architectural Recap

- **Screen / Visual:** Close print preview and return to dashboard overview.
- **Action:** Glance at the camera or judges with confident wrap-up.
- **Spoken Script:**
  > "To summarize our technical architecture:
  > - **Frontend:** React 18, Vite 5, Tailwind CSS, built-in vector print styles.
  > - **Backend:** Asynchronous FastAPI, Pydantic v2 validation, in-memory PyMuPDF document extraction.
  > - **Security:** Complete SSRF immunity—we never fetch or execute code from untrusted target websites; we only query public RDAP bootstrap endpoints and Cloudflare DNS-over-HTTPS.
  > - **Reliability:** Built-in deterministic rule fallback ensures full operation even during AI API outages.
  > 
  > OFFERPROOF gives students what they actually need: **Don't trust the offer. Verify the evidence.** Thank you, and I look forward to your questions."

---

## Section C — Judge-Facing Technical Architecture

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                  React 18 Frontend                                     │
│     Vite 5 • Tailwind CSS • Lucide Icons • In-Browser Media Print Vector Engine        │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │ HTTP / JSON REST API
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                   FastAPI Backend                                      │
│        Uvicorn ASGI • Python 3.10+ • Pydantic v2 • Strict CORS & Error Handling        │
└───────────────────┬───────────────────────┬───────────────────────┬────────────────────┘
                    │                       │                       │
      ┌─────────────┴──────────┐   ┌────────┴────────┐   ┌──────────┴──────────┐
      ▼                        ▼   ▼                 ▼   ▼                     ▼
┌───────────┐            ┌──────────────┐      ┌──────────────┐        ┌──────────────┐
│  PyMuPDF  │            │ Extraction   │      │ RDAP & DoH   │        │ Deterministic│
│ In-Memory │            │ Engine (AI + │      │ Evidence     │        │ Assessment   │
│PDF Parser │            │ Fallback)    │      │ Intelligence │        │ Engine       │
└───────────┘            └──────────────┘      └──────────────┘        └──────────────┘
```

### 1. Ingestion Layer (`app/services/ingestion.py`)
- **Text Ingestion:** Sanitizes whitespace, normalizes Unicode, strips potential injection characters, and parses external domain/hostname references without invoking network calls.
- **In-Memory PDF Ingestion:** Utilizes PyMuPDF (`fitz.open(stream=contents, filetype="pdf")`). Files are processed entirely in RAM without writing temporary files to the disk. Implements strict guards:
  - 5 MB maximum file upload size.
  - 10-page maximum document limit.
  - Verification of valid PDF magic bytes (`%PDF-`).
  - Graceful rejection of scanned image PDFs without OCR text layer.
- **SSRF Immunity:** Target URLs submitted by users are parsed strictly using Python's `urllib.parse` to extract hostnames and scheme metadata. Backend workers **never connect to, fetch HTML from, or execute code on the submitted URL**.

### 2. Claim Extraction Engine (`app/services/extraction.py`)
- **Structured Pydantic Schemas:** Employs `ClaimItem`, `ExtractedInformation`, `FinancialDetails`, and `RecruiterContact`.
- **Claim Isolation:** Breaks unstructured offers into atomic, verifiable claims (e.g., `organisation_name`, `domain_name`, `recruiter_email`, `application_fee`, `job_title`).
- **Pluggable AI & Deterministic Fallback:** 
  - AI extraction adapter supports Google Gemini (`gemini-1.5-flash`) or OpenAI endpoints.
  - If API keys are absent, rate-limited, or network fails, the system automatically falls back to an extensive deterministic regex/rule engine without crashing or throwing 500 errors.

### 3. Independent Evidence Verification (`app/services/verification.py`)
- **Authoritative RDAP Lookups:** Queries official ICANN RDAP bootstrap registries (`https://rdap.org/domain/{domain}`) over HTTPS. Computes exact domain age in days, flags newly registered domains ($<30$ days) or recent domains ($<180$ days), and extracts registrar information.
- **Cloudflare DNS-over-HTTPS (DoH):** Queries `https://cloudflare-dns.com/dns-query` with `application/dns-json` for `A`, `AAAA`, `MX`, `NS`, and `TXT` records safely over standard HTTPS ports, avoiding blocked UDP DNS port 53 traffic.
- **Email Consistency Engine:** Detects free consumer webmail domains (`gmail.com`, `yahoo.com`, `hotmail.com`, `outlook.com`) and cross-compares recruiter email domains against stated opportunity domains.
- **Evidence-to-Claim Mapping:** Evaluates claims into distinct statuses:
  - `supported`: Technical infrastructure confirms the claim (e.g. valid DNS routing matches domain).
  - `contradicted`: Technical evidence directly refutes the claim (e.g. non-existent domain name).
  - `inconclusive`: Evidence check failed or was ambiguous.
  - `not_checked`: **Strictly enforced** for claims that cannot be proven via public technical signals (salaries, stipends, job openings, fees).

### 4. Explainable Assessment & Safety Engine (`app/services/assessment.py`)
- **Categorization Hierarchy:**
  1. `high_caution`: Explicit upfront fee detected OR $\ge 2$ significant technical/linguistic inconsistencies.
  2. `needs_careful_review`: Exactly 1 significant concern (e.g. free email, domain age $<180$ days, or domain mismatch).
  3. `limited_concerns_detected`: Established domain ($>180$ days), enterprise email match, active DNS routing, no fees.
  4. `insufficient_evidence`: Sparse input data preventing technical lookups.
- **Actionable Findings:** Every finding includes `title`, `severity`, `explanation`, `why_it_matters`, `limitations`, `recommended_action`, and explicit arrays of `related_claim_ids` and `related_evidence_ids`.
- **Contextual Safety Recommendations:** Dynamically tailored guidance across Payment Safety, Identity Verification, Domain Integrity, and Personal Data Protection.

---

## Section D — Judge Q&A: 14 Anticipated Technical Questions & Answers

### Q1: "Why not simply feed the job description into a large language model and ask it if it's a scam?"
**Answer:**  
> "Feeding the prompt directly to an LLM creates two severe failure modes: **hallucination** and **stale ground truth**. 
> 
> An LLM cannot know whether `apex-innovations-tech.biz` was registered three days ago, nor can it check whether an MX record actually routes email today. LLMs are notoriously prone to manufacturing plausible-sounding company histories. 
> 
> In OFFERPROOF, the AI (when enabled) is restricted to an information extraction tool—extracting entities and atomic claims into a typed Pydantic schema. All verification and risk assessments are grounded in real, external, cryptographic and network evidence from RDAP and DNS-over-HTTPS. Even if the AI fails or is turned off, our deterministic fallback performs the exact same extraction."

---

### Q2: "How do you protect your backend from Server-Side Request Forgery (SSRF) when users submit links?"
**Answer:**  
> "We practice strict SSRF immunity by design: **our backend never fetches, scrapes, or visits submitted URLs**. 
> 
> When a user enters `http://malicious-internal-server.local/apply`, our ingestion service parses the string using Python's `urllib.parse` solely to extract structural tokens: the scheme (`http`), hostname, and domain. 
> 
> The only outbound HTTP requests our backend ever makes are to hardcoded, trusted public infrastructure APIs: the ICANN RDAP bootstrap server (`https://rdap.org`) and Cloudflare's public DNS-over-HTTPS service (`https://cloudflare-dns.com`). An attacker cannot force our server to probe local network interfaces or internal AWS metadata endpoints (`169.254.169.254`)."

---

### Q3: "Why doesn't OFFERPROOF assign a numeric scam probability, like '89% Risk of Fraud'?"
**Answer:**  
> "A numeric percentage implies a mathematical certainty and statistical calibration that does not exist. An '89% score' gives a false sense of precision, while a '15% score' might tempt a student to pay an advance fee because they think the risk is low. 
> 
> Instead, OFFERPROOF uses explainable guidance categories: `high_caution`, `needs_careful_review`, `limited_concerns_detected`, and `insufficient_evidence`. Every category is supported by auditable findings that clearly state: *What we found*, *Why it matters*, *What it does NOT prove*, and *What you should do*. We empower the candidate to make an informed decision rather than trusting an opaque number."

---

### Q4: "What happens if Cloudflare DoH or RDAP registries are down or rate-limiting your queries?"
**Answer:**  
> "Our evidence layer is architected with resilient asynchronous timeouts (3–5 seconds maximum per provider) using HTTPX. 
> 
> If an RDAP lookup times out or returns an HTTP 429/500, the system does not crash or fail the entire request. Instead, it marks that specific evidence item as `status="inconclusive"` with a human-readable explanation such as *'RDAP registry unavailable or timed out'*. 
> 
> The assessment engine then gracefully falls back: if insufficient evidence is gathered, it categorizes the opportunity as `insufficient_evidence` and explicitly instructs the candidate that technical registries could not be verified, advising them to take additional precautions."

---

### Q5: "How does OFFERPROOF behave if the AI API key is missing or the provider is offline?"
**Answer:**  
> "OFFERPROOF features a complete, zero-dependency **deterministic extraction fallback**. 
> 
> In `app/services/extraction.py`, the `_rule_based_extraction()` engine uses specialized regular expressions and linguistic heuristics to extract organizations, financial figures, upfront fee demands, recruiter emails, and application URLs. 
> 
> When `AI_PROVIDER=none` or when an API call fails, the fallback engages seamlessly in milliseconds. The rest of the pipeline—evidence verification, claim mapping, and explainable assessment—runs identically. In fact, our automated test suite runs 100% in deterministic fallback mode to ensure rock-solid CI/CD reliability."

---

### Q6: "Can a scammer bypass your system by using an aged, established domain or registering a custom email?"
**Answer:**  
> "Yes, and that is precisely why our platform explicitly differentiates between **technical consistency** and **opportunity legitimacy**. 
> 
> If a scammer hacks an old domain or registers `legit-sounding-corp.com`, our system will verify that the domain is old and has DNS records. However, if the scammer demands a ₹2,000 security deposit or registration fee, the assessment engine **still triggers High Caution** because upfront fees violate recruitment safety standards regardless of domain age. 
> 
> Furthermore, in the report, we explicitly warn the student: *'An established domain confirms registration age, but does not verify whether the recruiter is authorized or whether the job vacancy is genuine.'*"

---

### Q7: "What about legitimate early-stage startups that registered their domain last month or use Gmail for hiring?"
**Answer:**  
> "We specifically designed our categories to avoid false accusations of fraud. If a genuine startup has a 20-day-old domain or uses Gmail, OFFERPROOF does not call them a 'scam'. It assigns **Needs careful review** with a finding labeled `severity: "caution"`. 
> 
> The explanation states clearly: *'Early-stage companies and legitimate small teams sometimes use free email services or newly launched domains.'* 
> 
> The recommended action does not tell the student to report them, but rather: *'Request an introductory video call or confirm the opportunity through the founder's verified LinkedIn profile before sharing private documents.'*"

---

### Q8: "How does the PDF ingestion work, and how do you protect against malicious PDF files or zip bombs?"
**Answer:**  
> "PDF parsing is handled in-memory using PyMuPDF (`fitz`), which is a fast, C-based parsing engine. 
> 
> We implement a four-tiered defense:
> 1. **Size check:** Reject any file over 5 MB immediately before parsing.
> 2. **Magic bytes:** Verify that the stream begins with `%PDF-`.
> 3. **Page limit:** PyMuPDF checks `doc.page_count`; if it exceeds 10 pages, we reject it to prevent CPU exhaustion.
> 4. **No disk writes:** The bytes remain strictly in a temporary memory buffer and are closed immediately after text extraction. If a PDF contains only scanned bitmaps without text, we return a 422 error advising the user to upload a text-based PDF or paste the text directly."

---

### Q9: "Why are salaries, stipends, and job openings strictly marked as `not_checked`?"
**Answer:**  
> "Because there is no public technical protocol in existence that can cryptographically verify an internal corporate opening or salary offer. 
> 
> RDAP tells us who owns a domain name. DNS tells us where web traffic and mail route. Neither can confirm that 'Apex Innovations' has an open budget for a ₹35,000/month intern. 
> 
> In traditional tools, systems falsely imply that if an email is real, the job must be real. We explicitly mark those claims as `not_checked` to keep the student vigilant and remind them to independently verify the job posting on the company's official careers portal."

---

### Q10: "How does the claim extraction engine separate entities from claims and indicators?"
**Answer:**  
> "We enforce a three-layer schema in Pydantic:
> 1. **Entities (`ExtractedInformation`):** High-level organizational and opportunity attributes (company name, role title, salary strings, contact emails).
> 2. **Atomic Claims (`ClaimItem`):** Factual assertions that could theoretically be checked against evidence (e.g. *'The organisation website domain is example.com'*, *'The recruiter email is recruiter@example.com'*). Each claim has a unique ID (`claim_001`), claim category, and initial `verification_status: not_checked`.
> 3. **Suspicious Indicators (`SuspiciousIndicator`):** Linguistic or structural anomalies extracted directly from the raw text (e.g., upfront payment demands, urgency tactics, confidentiality warnings)."

---

### Q11: "How does OFFERPROOF safeguard student privacy and personal data?"
**Answer:**  
> "First, we do not require user accounts, logins, or cookies to use the platform. 
> 
> Second, our system is designed to analyze **opportunity announcements**, not applicant identities. We include prominent warnings reminding users **never to paste personal identification details**, banking information, or passwords into the system. 
> 
> Third, all document parsing is transient and stateless: text and PDF bytes reside in volatile memory for the duration of the analysis request and are discarded immediately upon JSON response delivery."

---

### Q12: "How could a university career center or college placement cell integrate OFFERPROOF?"
**Answer:**  
> "OFFERPROOF is architected as an API-first platform. A university placement portal or student LMS can integrate our `/api/v1/analyze` endpoint directly into their employer registration workflow. 
> 
> When an unknown recruiter submits a campus drive application, the university can automatically run the announcement through OFFERPROOF. If the recruiter's email domain doesn't match the company domain, or if the website was registered last week, the system flags the listing for manual advisor review. 
> 
> Additionally, career advisors can use our **'Print / Save PDF'** feature as a standard due-diligence scorecard when advising students about suspicious off-campus offers."

---

### Q13: "How does the frontend generate the printable PDF report without server-side rendering or heavy external libraries?"
**Answer:**  
> "We engineered custom CSS print media stylesheets (`@media print`) paired with dedicated React report layout components. 
> 
> When the user clicks **'Print / Save PDF'**, the browser triggers its native high-fidelity print engine (`window.print()`). This approach has zero server rendering overhead, requires no heavy canvas or headless Chrome dependencies (like Puppeteer), renders razor-sharp vector typography and icons at 300+ DPI, and generates a standards-compliant PDF directly through the user's native operating system print dialog."

---

### Q14: "What are the limitations of the current implementation and what would Phase 6 look like?"
**Answer:**  
> "Currently, OFFERPROOF evaluates public domain infrastructure, DNS records, and email domain consistency. 
> 
> Our future Phase 6 roadmap includes:
> 1. **Direct `.eml` Header Analysis:** Allowing students to drag-and-drop original email files to inspect SPF, DKIM, and DMARC cryptographic signatures to detect email spoofing.
> 2. **Corporate Registry API Connectors:** Cross-referencing official government business databases (such as India's MCA/ROC, UK Companies House, or US SEC EDGAR) to verify corporate registration numbers.
> 3. **University Career Portal Plugins:** Browser extensions allowing students to verify job postings directly on platforms like LinkedIn, Indeed, or Handshake."

---

## Section E — Presentation Backup & Contingency Plan

During a live hackathon demonstration, external dependencies can occasionally fail. Here is the exact backup strategy:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        LIVE DEMO CONTINGENCY MATRIX                    │
├──────────────────────────┬──────────────────────┬──────────────────────┤
│ Scenario                 │ Root Cause           │ Immediate Contingency│
├──────────────────────────┼──────────────────────┼──────────────────────┤
│ Local backend not        │ Port collision or    │ Run `run_demo.bat`   │
│ responding               │ process termination  │ to auto-restart venv │
├──────────────────────────┼──────────────────────┼──────────────────────┤
│ External Wi-Fi is        │ Slow conference Wi-Fi│ Deterministic engine │
│ down or lagging          │ or blocked DNS ports │ returns fast fallback│
├──────────────────────────┼──────────────────────┼──────────────────────┤
│ Browser cache or local   │ Outdated state in    │ Press Ctrl+F5 or use │
│ Vite port conflict       │ local browser tab    │ Incognito window     │
└──────────────────────────┴──────────────────────┴──────────────────────┘
```

### Contingency 1: Backend Server Fails to Start or Terminates
- **Action:** Open terminal and run `run_demo.bat` directly from the repository root.
- **Manual Command:**
  ```powershell
  cd c:\Users\sanja\project\CONTEST\DEVPOST\OFFERPROOF\backend
  .\.venv\Scripts\Activate.ps1
  python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
  ```
- **Validation:** Open `http://127.0.0.1:8000/api/v1/health` in a browser. It should return `{"status": "healthy"}`.

### Contingency 2: External RDAP or Cloudflare DoH Requests Hang
- **Explanation to Judges:**  
  > *"Notice how gracefully OFFERPROOF handles network latency: external network calls are wrapped in 3-second strict timeouts. Even if an upstream domain registry experiences latency, our system safely flags the check as 'inconclusive' and continues rendering the assessment without crashing."*

### Contingency 3: AI Provider Key is Not Configured
- **No problem:** OFFERPROOF is designed by default to operate in `AI_PROVIDER=none` mode using the deterministic rule-based extractor. 
- **Explanation to Judges:**  
  > *"We deliberately engineered OFFERPROOF to run reliably without third-party AI API keys. Our deterministic extraction engine extracts entities, fees, and claims using high-precision rules, guaranteeing zero vendor lock-in and zero downtime."*

### Contingency 4: Demo Walkthrough Sample Button Not Responding
- **Manual Input:** You can paste the following text into the input textarea:
  ```text
  Subject: Urgent: Machine Learning Internship Offer - Apex Innovations

  Dear Applicant,

  We are pleased to offer you a remote Machine Learning Internship at Apex Innovations starting immediately.
  The monthly stipend is Rs. 35,000 for a duration of 3 months.

  To confirm your acceptance, you must submit a refundable laptop security deposit and onboarding fee of Rs. 1,500 within 48 hours to secure your equipment.

  Please send your confirmation to careers.apex.internship@gmail.com and visit our official website at http://apex-innovations-tech.biz to complete your onboarding registration.

  Sincerely,
  Recruitment Team, Apex Innovations
  ```

---

## Section F — Final Pre-Flight Checklist

Complete this checklist 15 minutes before presenting to judges:

- [ ] **1. Clean Terminal & Environment:**
  - Close any orphaned Node or Python processes (`taskkill /F /IM python.exe` and `taskkill /F /IM node.exe` if necessary).
- [ ] **2. Launch via Batch File:**
  - Double-click `run_demo.bat` in the repository root.
  - Verify two command windows appear:
    - `OFFERPROOF - Backend API (FastAPI)`
    - `OFFERPROOF - Frontend Web UI (Vite)`
- [ ] **3. Verify Backend Health:**
  - Open `http://127.0.0.1:8000/api/v1/health` in your browser.
  - Confirm response status is `"healthy"`.
- [ ] **4. Verify Frontend Dashboard:**
  - Open `http://localhost:5173`.
  - Confirm title, badges, and layout render crisply.
- [ ] **5. Test the Demo Walkthrough Button:**
  - Click **"Demo Walkthrough"**.
  - Confirm input textarea populates with the Apex Innovations scenario.
  - Click **"Analyze & Verify Opportunity"**.
  - Confirm the **High caution** banner, findings cards, and evidence chips appear in under 2 seconds.
- [ ] **6. Test the Print / Save PDF Feature:**
  - Click the **"Print / Save PDF"** button.
  - Verify the report modal preview opens cleanly with header, report ID, timestamp, and findings.
  - Press `Esc` or click the close icon to return to the dashboard.
- [ ] **7. Browser Zoom & Display Setup:**
  - Set browser zoom to 100% or 110% for optimal readability on projection screens.
  - Close unrelated browser tabs, bookmarks bar, and desktop notifications.
- [ ] **8. Audio & Mic Check:**
  - Test microphone clarity if presenting remotely on Zoom / Google Meet / Discord.
- [ ] **9. Time Management:**
  - Keep a stopwatch or phone timer ready for the 3-minute limit.
- [ ] **10. Mindset:**
  - Speak with measured confidence. Emphasize evidence, transparency, and safety over buzzwords.

