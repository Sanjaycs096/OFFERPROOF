import sys
import io
import asyncio
from pathlib import Path

backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

import pymupdf
from httpx import ASGITransport, AsyncClient
from app.main import app


def create_in_memory_pdf(text: str = "Test offer document") -> bytes:
    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text((50, 72), text)
    data = doc.tobytes()
    doc.close()
    return data


async def run_ingestion_api_tests():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        # 1. Test Phase 1 Root & Health preservation
        res_root = await client.get("/")
        assert res_root.status_code == 200
        assert res_root.json()["version"] == "0.5.0"
        print("[PASS] GET / preserved.")

        res_h = await client.get("/health")
        assert res_h.status_code == 200
        print("[PASS] GET /health preserved.")

        # 2. Test Versioned API v1 Health
        res_v1_health = await client.get("/api/v1/health")
        assert res_v1_health.status_code == 200
        v1_data = res_v1_health.json()
        assert v1_data["status"] == "ok"
        assert v1_data["features"]["text_ingestion"] is True
        assert v1_data["features"]["pdf_ingestion"] is True
        assert v1_data["features"]["claim_extraction"] is True
        print("[PASS] GET /api/v1/health passed:", v1_data)

        # 3. Test Valid Text Ingestion
        res_text = await client.post(
            "/api/v1/ingest/text",
            json={
                "text": "Software Engineering Internship at CloudScale Technologies. Stipend $3,000/mo.",
                "url": "https://cloudscale.example.com/apply/intern",
                "category_hint": "internship",
            },
        )
        assert res_text.status_code == 200
        t_data = res_text.json()
        assert t_data["success"] is True
        assert t_data["source_type"] == "text"
        assert t_data["url_metadata"]["hostname"] == "cloudscale.example.com"
        print("[PASS] POST /api/v1/ingest/text passed.")

        # 4. Test Empty Text Ingestion (Validation Error)
        res_empty_text = await client.post(
            "/api/v1/ingest/text",
            json={"text": "   ", "url": None},
        )
        assert res_empty_text.status_code in [400, 422]
        print("[PASS] Empty text rejected with status:", res_empty_text.status_code)

        # 5. Test Valid PDF Ingestion
        pdf_bytes = create_in_memory_pdf("Offer of Employment from Horizon Systems. Pay $75,000/yr.")
        files = {
            "file": ("horizon_offer.pdf", pdf_bytes, "application/pdf"),
        }
        data = {"url": "https://horizon.example.com"}
        res_pdf = await client.post("/api/v1/ingest/pdf", files=files, data=data)
        assert res_pdf.status_code == 200
        pdf_resp = res_pdf.json()
        assert pdf_resp["success"] is True
        assert pdf_resp["source_type"] == "pdf"
        assert "Horizon Systems" in pdf_resp["content"]
        assert pdf_resp["document_metadata"]["page_count"] == 1
        assert pdf_resp["url_metadata"]["hostname"] == "horizon.example.com"
        print("[PASS] POST /api/v1/ingest/pdf valid upload passed.")

        # 6. Test Invalid PDF Upload (Wrong header / corrupt)
        fake_files = {
            "file": ("corrupt.pdf", b"NOT_A_VALID_PDF_STREAM", "application/pdf"),
        }
        res_bad_pdf = await client.post("/api/v1/ingest/pdf", files=fake_files)
        assert res_bad_pdf.status_code == 422
        print("[PASS] Invalid PDF header rejected with status 422.")

        # 7. Test Empty PDF Upload (0 text)
        empty_doc = pymupdf.open()
        empty_doc.new_page()
        empty_bytes = empty_doc.tobytes()
        empty_doc.close()
        empty_files = {
            "file": ("empty.pdf", empty_bytes, "application/pdf"),
        }
        res_empty_pdf = await client.post("/api/v1/ingest/pdf", files=empty_files)
        assert res_empty_pdf.status_code == 422
        assert "No selectable text" in res_empty_pdf.json()["detail"]
        print("[PASS] Empty/scanned PDF rejected with status 422.")

        # 8. Test End-to-End Extraction API
        res_extract = await client.post(
            "/api/v1/extract",
            json={
                "content": (
                    "Congratulations! You have been selected for a Data Science Internship at ABC Technologies. "
                    "Earn ₹45,000 per month. Pay ₹1,500 as a registration fee before October 31. Guaranteed selection."
                ),
                "source_type": "text",
                "application_url": "https://abctech.example.com/apply",
            },
        )
        assert res_extract.status_code == 200
        ext_data = res_extract.json()
        assert ext_data["success"] is True
        assert ext_data["extraction_mode"] in ["ai", "rule_based"]
        assert ext_data["extracted_information"]["organisation"]["name"] == "ABC Technologies"
        assert len(ext_data["claims"]) >= 5
        # Verify EVERY claim has verification_status == 'not_checked'
        for c in ext_data["claims"]:
            assert c["verification_status"] == "not_checked"
        print(f"[PASS] POST /api/v1/extract passed with {len(ext_data['claims'])} claims.")

    print("\nALL INGESTION API TESTS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    asyncio.run(run_ingestion_api_tests())
