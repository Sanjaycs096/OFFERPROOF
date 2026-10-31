# OFFERPROOF — Hackathon Submission & Judge Presentation Kit

> **Tagline:** Don't trust the offer. Verify the evidence.  
> **Repository:** [https://github.com/Sanjaycs096/OFFERPROOF.git](https://github.com/Sanjaycs096/OFFERPROOF.git)  
> **Release Version:** `0.5.0` (Production Hardened)

---

## 1. Project Overview & Quick Summary

- **What is OFFERPROOF?**  
  An AI-assisted, evidence-grounded opportunity verification platform that helps students and job seekers evaluate job offers, internship announcements, and scholarship notices.
- **The Core Problem:**  
  Students frequently receive deceptive employment offers demanding upfront fees, impersonating reputable enterprises through lookalike domains, or using untraceable consumer webmail. Existing tools rely on black-box predictions, opaque spam filters, or superficial reviews.
- **The OFFERPROOF Solution:**  
  Rather than guessing or manufacturing certainty, OFFERPROOF isolates extracted opportunity claims, cross-references independent technical infrastructure evidence (RDAP domain registration, Cloudflare DNS-over-HTTPS, and email protocol alignment), and delivers explainable assessment findings with prioritized next steps.
- **The Core Principle:**  
  *OFFERPROOF must help students make safer decisions by showing the evidence, explaining the concerns, and identifying what remains unknown. It must never manufacture certainty.*

---

## 2. 60-Second Elevator Pitch

> *"Every semester, thousands of college students fall victim to employment and scholarship scams. A student receives an exciting email: 'Congratulations! You've been selected for a remote Machine Learning Internship paying ₹35,000/month. Just pay a ₹1,500 registration or equipment fee to secure your onboarding.'*  
>  
> *Students don't know who to trust, and existing scam checkers only offer black-box percentages like '87% scam risk' without showing any proof.*  
>  
> *OFFERPROOF changes this paradigm with our tagline: **Don't trust the offer. Verify the evidence.***  
>  
> *When a student pastes an offer text or uploads an offer PDF, OFFERPROOF decomposes the document into verifiable claims. It checks authoritative public infrastructure records—RDAP domain registration age, Cloudflare DNS-over-HTTPS routing, and recruiter email domain consistency—without ever executing or scraping untrusted links. Most importantly, it clearly separates verified technical facts from unverified terms like salaries and hiring promises, providing students with prioritized, actionable guidance before they send money or disclose private data."*

---

## 3. Three-Minute Live Demonstration Script

### Timing & Scene Breakdown

| Timestamp | Screen / Action | Spoken Demonstration Narrative |
| :--- | :--- | :--- |
| **0:00 – 0:30** | **Landing Page Hero** | "Welcome to OFFERPROOF. The first screen immediately highlights our mission: helping students bridge the gap between deceptive recruitment copy and verifiable organizational reality. Notice our tagline: *'Don't trust the offer. Verify the evidence.'* We do not generate synthetic risk scores or claim 100% fraud detection; we provide transparent, evidence-grounded decision intelligence." |
| **0:30 – 1:15** | **One-Click Demo Sample Loading** | "Let's test a realistic scenario. I'll click **'Demo Walkthrough'** to load a synthetic demonstration opportunity: a Machine Learning Internship claiming ₹35,000/month stipend at 'Apex Innovations', with a recruiter using a consumer `@gmail.com` address, asking for an upfront ₹1,500 registration fee before an urgent deadline. We hit **'Analyze & Verify Opportunity'**." |
| **1:15 – 1:55** | **Analysis & Claim Extraction** | "Behind the scenes, OFFERPROOF ingests the text, decomposes the announcement into atomic claims, and immediately queries public RDAP registries and Cloudflare DNS-over-HTTPS. In seconds, the Opportunity Assessment dashboard renders. Notice the assessment guidance category: **High caution**." |
| **1:55 – 2:35** | **Findings & Traceability** | "Look at the findings. Finding 1 highlights the upfront ₹1,500 registration fee. We explain why it matters, what it does NOT prove, and the recommended action: never pay advance fees. Finding 2 observes that the recruiter is operating from public webmail rather than an enterprise domain. Below, we clearly contrast **What We Verified** (domain age, DNS A records) with **What Remains Unverified** (stipend amount, hiring selection, vacancy availability)." |
| **2:35 – 3:00** | **Safety Checklist & Printable PDF** | "Finally, the student receives a prioritized next-steps checklist. With one click on **'Print / Save PDF'**, OFFERPROOF compiles a clean, printable due-diligence report complete with official branding, Report ID, timestamp, and methodology disclaimers to take to a university career advisor." |

---

## 4. Judge-Facing Technical Architecture

```
                               ┌────────────────────────────────────────────────────────┐
                               │                    React 18 Frontend                   │
                               │           Vite 5 • Tailwind CSS • Lucide Icons         │
                               └───────────────────────────┬────────────────────────────┘
                                                           │ JSON REST API
                                                           ▼
                               ┌────────────────────────────────────────────────────────┐
                               │                   FastAPI Backend                      │
                               │        Uvicorn ASGI • Pydantic v2 Validation           │
                               └───────┬───────────────────┬───────────────────┬────────┘
                                       │                   │                   │
                     ┌─────────────────┴──┐      ┌─────────┴─────────┐     ┌───┴────────────────┐
                     ▼                    ▼      ▼                   ▼     ▼                    ▼
             ┌───────────────┐   ┌────────────┐┌───────────────┐┌─────────┐┌───────────────────┐
             │ PyMuPDF (PDF) │   │ AI Provider││ RDAP Registry ││Cloudfl. ││ Assessment Engine │
             │ In-Memory Text│   │ / Fallback ││ Domain Intel  ││ DoH DNS ││ Deterministic     │
             └───────────────┘   └────────────┘└───────────────┘└─────────┘└───────────────────┘
```

### 1. Ingestion Layer
- Accepts pasted text, direct URLs, or text-based PDF documents.
- PDF parsing operates in-memory via PyMuPDF (`fitz`) with strict size limits (5 MB) and page limits (10 pages).
- **SSRF Immunity:** Target URLs are structurally parsed for domain/host metadata only; backend workers **never visit, download, or execute code from untrusted target websites**.

### 2. Claim Extraction Engine
- Extracts structured entities (organisation, opportunity, financial terms, recruiter contacts).
- Isolates verifiable atomic claims with source text offsets and confidence ratings.
- **Pluggable AI & Deterministic Fallback:** Modular provider abstraction supports Gemini API (`gemini-1.5-flash`) or OpenAI-compatible endpoints. When credentials are unavailable or rate-limited, deterministic rule-based regex extraction engages seamlessly with zero disruption.

### 3. Independent Technical Evidence Layer
- **RDAP Domain Intelligence:** Queries authoritative RDAP bootstrap services over HTTPS (`https://rdap.org/domain`) to extract domain creation timestamps, calculate age in days, and flag newly registered domains ($<30$ days) or recent registrations ($30\text{--}180$ days).
- **DNS-over-HTTPS (DoH):** Queries Cloudflare DoH endpoints (`https://cloudflare-dns.com/dns-query`) for `A`, `AAAA`, `MX`, `NS`, and `TXT`/`SPF` records safely without arbitrary UDP packet transmission.
- **Email Consistency Engine:** Detects free consumer webmail (`gmail.com`, `yahoo.com`, `outlook.com`) and cross-compares recruiter domains against opportunity websites.

### 4. Explainable Assessment & Safety Recommendation Engine
- Deterministic categorization rules assigning one of four guidance levels:
  - `high_caution`
  - `needs_careful_review`
  - `limited_concerns_detected`
  - `insufficient_evidence`
- Generates contextual safety recommendations (Payment safety, Personal data protection, Recruiter identity confirmation, Domain integrity).
- Compiles prioritized, ordered student next steps.

---

## 5. Innovation & Competitive Differentiation

| Traditional Job Scanners | Generic AI Prompt Wrappers | OFFERPROOF Verification Platform |
| :--- | :--- | :--- |
| Black-box percentage score (e.g. "92% risk") with no supporting evidence. | Prone to hallucinations; treats text claims as verified ground truth. | **Claim-level evidence mapping:** Every finding references explicit technical evidence and claim IDs. |
| Crawls user URLs risking SSRF, malware, or credential phishing exposure. | No live external technical checks; only reads the text provided. | **SSRF-safe technical intelligence:** Checks RDAP & Cloudflare DoH without touching destination servers. |
| Declares offers as definitively "legitimate" or "fraudulent". | Fabricates certainty; invents nonexistent company affiliations. | **Transparent uncertainty:** Clearly separates verified technical facts from unverified terms (salaries, openings). |
| Static advice not tailored to the specific opportunity claims. | Generic AI responses without structured due-diligence checklists. | **Prioritized action plan:** Actionable next steps and printable due-diligence reports for students. |

---

## 6. Real-World Student Impact

- **Financial Loss Prevention:** Protects students from paying upfront "equipment deposits", "visa fees", or "training registration fees" that account for millions in annual student recruitment losses.
- **Identity Theft Mitigation:** Informs job seekers when not to disclose Social Security Numbers, bank credentials, or passport scans.
- **Empowered Due Diligence:** Equips career counseling centers, universities, and students with transparent, verifiable inspection scorecards that can be saved as vector PDF documents.

