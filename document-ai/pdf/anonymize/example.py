#!/usr/bin/env python3
"""PaperOffice AI — GDPR-compliant anonymization of documents

Automatically redacts personal data in PDFs and images.
Template: document_anonymize | Param: file (not file_1!)

Usage:
    export PAPEROFFICE_API_KEY=po_ut_xxx
    python3 example.py document.pdf [categories]

Categories: all, names, addresses, phone, email, iban, tax_id
"""
import os
import sys
import requests

def wait_for_result(data: dict, token: str, api_base: str = "https://api.paperoffice.ai/latest", timeout_s: int = 180) -> dict:
    """HTTP 202 means the job is still running: follow job/get until it is completed."""
    if data.get("result") or not data.get("job_id"):
        return data
    import time
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        time.sleep(2)
        poll = requests.get(f"{api_base}/job/get/{data['job_id']}", headers={"Authorization": f"Bearer {token}"}).json()
        if poll.get("job_status") == "completed" or poll.get("result") or poll.get("job_result"):
            # job/get returns the payload as job_result — expose it under result like the inline response
            if "result" not in poll and "job_result" in poll:
                poll["result"] = poll["job_result"]
            return poll
        if poll.get("job_status") in ("failed", "error") or poll.get("status") == "error":
            raise RuntimeError(f"job failed: {poll.get('message')}")
    raise TimeoutError(f"job {data['job_id']} not finished after {timeout_s}s")


api_base = "https://api.paperoffice.ai/latest"
api_key = os.environ.get("PAPEROFFICE_API_KEY")
if not api_key:
    sys.exit("Error: PAPEROFFICE_API_KEY not set")

input_file = sys.argv[1] if len(sys.argv) > 1 else None
if not input_file:
    sys.exit("Usage: python3 example.py <document.pdf> [categories]")

redact_categories = sys.argv[2] if len(sys.argv) > 2 else "all"

print(f"→ Anonymizing: {input_file} (categories: {redact_categories})")

with open(input_file, "rb") as f:
    response = requests.post(
        f"{api_base}/job/add/workflow",
        headers={"Authorization": f"Bearer {api_key}"},
        files={"file": f},
        data={
            "template": "document_anonymize",
            "redact_categories": redact_categories,
            "processing_lane": "instant",
        },
    )

data = wait_for_result(response.json(), api_key)
print(f"Status: {data.get('status')}")

if data.get("status") != "success":
    print(f"Error: {data}")
    sys.exit(1)

result = data.get("result", {})
download_urls = result.get("anonymized_pdf", result.get("files", []))
if not download_urls:
    sys.exit("Error: No download URL received")

pii = result.get("detected_pii", {})
if pii:
    audit = pii.get("audit_trail", [])
    print(f"Redacted entities: {len(audit)}")
    for entry in audit[:5]:
        print(f"  [{entry.get('category')}] {entry.get('reason', '')[:60]}")

dl_response = requests.get(
    download_urls[0],
    headers={"Authorization": f"Bearer {api_key}"},
)

with open("anonymized.pdf", "wb") as out:
    out.write(dl_response.content)

print(f"Saved as: anonymized.pdf ({len(dl_response.content)} bytes)")
