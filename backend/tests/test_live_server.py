import subprocess
import time
import sys
import urllib.request
import json


def test_live_server():
    python_exe = sys.executable
    print(f"Starting uvicorn server with {python_exe}...")
    proc = subprocess.Popen(
        [python_exe, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"],
        cwd="backend",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    try:
        # Give server time to bind and listen
        time.sleep(2.5)

        # 1. Test Root Endpoint
        req_root = urllib.request.Request("http://127.0.0.1:8000/")
        with urllib.request.urlopen(req_root, timeout=5) as res:
            assert res.status == 200
            data = json.loads(res.read().decode())
            print("[PASS] HTTP Live Server Root GET /:", data)

        # 2. Test Health Endpoint
        req_health = urllib.request.Request("http://127.0.0.1:8000/health")
        with urllib.request.urlopen(req_health, timeout=5) as res:
            assert res.status == 200
            data = json.loads(res.read().decode())
            print("[PASS] HTTP Live Server Health GET /health:", data)

        # 3. Test API v1 Health Endpoint
        req_v1_health = urllib.request.Request("http://127.0.0.1:8000/api/v1/health")
        with urllib.request.urlopen(req_v1_health, timeout=5) as res:
            assert res.status == 200
            data = json.loads(res.read().decode())
            print("[PASS] HTTP Live Server API v1 Health GET /api/v1/health:", data)

        # 4. Test Text Ingestion via HTTP POST
        ingest_payload = json.dumps({
            "text": "Selected for Data Analyst at TechCorp. Salary: $65/hr. Apply at https://techcorp.example.com",
            "url": "https://techcorp.example.com/apply"
        }).encode("utf-8")
        req_ingest = urllib.request.Request(
            "http://127.0.0.1:8000/api/v1/ingest/text",
            data=ingest_payload,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req_ingest, timeout=5) as res:
            assert res.status == 200
            data = json.loads(res.read().decode())
            assert data["success"] is True
            print("[PASS] HTTP Live Server POST /api/v1/ingest/text:", data["message"])

        # 5. Test Claim Extraction via HTTP POST
        extract_payload = json.dumps({
            "content": "Congratulations! You have been selected for a Data Science Internship at ABC Technologies. Earn ₹45,000 per month. Pay ₹1,500 as a registration fee before October 31. Guaranteed selection.",
            "source_type": "text",
            "application_url": "https://abctech.example.com/apply",
            "force_mode": "rule_based"
        }).encode("utf-8")
        req_extract = urllib.request.Request(
            "http://127.0.0.1:8000/api/v1/extract",
            data=extract_payload,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req_extract, timeout=5) as res:
            assert res.status == 200
            data = json.loads(res.read().decode())
            assert data["success"] is True
            assert len(data["claims"]) >= 5
            for c in data["claims"]:
                assert c["verification_status"] == "not_checked"
            print(f"[PASS] HTTP Live Server POST /api/v1/extract: Extracted {len(data['claims'])} claims, all marked 'not_checked'.")

        # 6. Test Evidence Verification via HTTP POST (Phase 3)
        verify_payload = json.dumps({
            "extracted_information": {
                "organisation": {"name": "ABC Technologies", "website": "https://abctech.example.com"},
                "opportunity": {"role": "Data Science Internship"},
                "financial_details": {"stipend": "₹45,000 per month", "registration_fees": "₹1,500"},
                "recruiter": {"email": "recruiter@gmail.com"},
                "application": {"application_url": "https://abctech.example.com/apply"}
            },
            "claims": [
                {
                    "claim_id": "CLM-001",
                    "claim_text": "Organisation claims to be ABC Technologies.",
                    "claim_category": "organisation",
                    "source_text": "ABC Technologies",
                    "confidence": 0.9,
                    "verification_status": "not_checked"
                },
                {
                    "claim_id": "CLM-002",
                    "claim_text": "Advertised monthly stipend is ₹45,000 per month.",
                    "claim_category": "financial",
                    "source_text": "₹45,000 per month",
                    "confidence": 0.9,
                    "verification_status": "not_checked"
                }
            ],
            "source_type": "text",
            "application_url": "https://abctech.example.com/apply"
        }).encode("utf-8")
        req_verify = urllib.request.Request(
            "http://127.0.0.1:8000/api/v1/verify",
            data=verify_payload,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req_verify, timeout=8) as res:
            assert res.status == 200
            data = json.loads(res.read().decode())
            assert data["success"] is True
            assert len(data["evidence"]) >= 3
            assert data["verification_summary"]["not_checked"] >= 1
            print(f"[PASS] HTTP Live Server POST /api/v1/verify: Processed {len(data['evidence'])} evidence items.")

        print("\n[SUCCESS] Live Uvicorn server successfully handled Phase 1, Phase 2, and Phase 3 endpoints over HTTP!")
    finally:
        print("Stopping uvicorn server...")
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            proc.kill()
        print("Server stopped cleanly.")


if __name__ == "__main__":
    test_live_server()
