import asyncio
import sys
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from httpx import ASGITransport, AsyncClient
from app.main import app


async def run_tests():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        # Test Root Endpoint
        res_root = await client.get("/")
        print("Root Status:", res_root.status_code)
        print("Root Response:", res_root.json())
        assert res_root.status_code == 200
        root_data = res_root.json()
        assert "message" in root_data
        assert root_data["tagline"] == "Don't trust the offer. Verify the evidence."
        assert root_data["health_url"] == "/health"
        assert root_data["docs_url"] == "/docs"
        assert root_data["version"] == "0.3.0"

        # Test Health Endpoint
        res_health = await client.get("/health")
        print("\nHealth Status:", res_health.status_code)
        print("Health Response:", res_health.json())
        assert res_health.status_code == 200
        health_data = res_health.json()
        assert health_data["status"] == "ok"
        assert health_data["service"] == "offerproof-api"
        assert health_data["version"] == "0.3.0"
        assert "timestamp" in health_data

        # Test CORS Preflight
        res_cors = await client.options(
            "/health",
            headers={
                "Origin": "http://localhost:5173",
                "Access-Control-Request-Method": "GET",
            },
        )
        print("\nCORS Status:", res_cors.status_code)
        print("CORS Origin Header:", res_cors.headers.get("access-control-allow-origin"))
        assert res_cors.status_code == 200
        assert res_cors.headers.get("access-control-allow-origin") == "http://localhost:5173"

        # Test POST /api/v1/verify
        verify_payload = {
            "extracted_information": {
                "organisation": {"name": "Apex Tech", "website": "https://apex-tech.example.com"},
                "opportunity": {"role": "Python Developer"},
                "financial_details": {"salary": "$80,000"},
                "recruiter": {"email": "recruiter@gmail.com"},
                "application": {"application_url": "https://apex-tech.example.com/apply"}
            },
            "claims": [
                {
                    "claim_id": "CLM-001",
                    "claim_text": "Organisation claims to be Apex Tech.",
                    "claim_category": "organisation",
                    "source_text": "Apex Tech",
                    "confidence": 0.9,
                    "verification_status": "not_checked"
                },
                {
                    "claim_id": "CLM-002",
                    "claim_text": "Salary is $80,000.",
                    "claim_category": "financial",
                    "source_text": "$80,000",
                    "confidence": 0.9,
                    "verification_status": "not_checked"
                }
            ],
            "source_type": "text",
            "application_url": "https://apex-tech.example.com/apply"
        }
        res_v = await client.post("/api/v1/verify", json=verify_payload)
        assert res_v.status_code == 200
        v_data = res_v.json()
        assert v_data["success"] is True
        assert len(v_data["claims"]) == 2
        # Check that financial claim is not_checked
        fin_c = [c for c in v_data["claims"] if c["claim_category"] == "financial"][0]
        assert fin_c["verification_status"] == "not_checked"
        assert len(v_data["evidence"]) >= 3
        print("\n[PASS] POST /api/v1/verify passed.")

        # Test POST /api/v1/analyze
        analyze_payload = {
            "content": "Data Analyst role at Nexus Technologies. Earn ₹50,000 per month. Contact hr@nexus.example.com. Apply at https://nexus.example.com/apply",
            "source_type": "text",
            "application_url": "https://nexus.example.com/apply",
            "force_mode": "rule_based"
        }
        res_a = await client.post("/api/v1/analyze", json=analyze_payload)
        assert res_a.status_code == 200
        a_data = res_a.json()
        assert a_data["success"] is True
        assert a_data["verification_summary"]["total_claims"] >= 3
        print("[PASS] POST /api/v1/analyze passed.")

    print("\n[PASS] ALL BACKEND TESTS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    asyncio.run(run_tests())
