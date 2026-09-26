#!/usr/bin/env python3
"""PaperOffice AI — Intelligent PDF splitting with AI detection"""
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
    sys.exit("Error: Please provide file path as argument")

# Upload PDF and split using AI
with open(input_file, "rb") as f:
    response = requests.post(
        f"{api_base}/job/add/workflow",
        headers={"Authorization": f"Bearer {api_key}"},
        files={"file": (os.path.basename(input_file), f)},
        data={
            "template": "pdf_ai_split",
            "naming_instruction": "Name by document type and date",
            "processing_lane": "instant",
        },
    )

data = wait_for_result(response.json(), api_key)
print(f"Status: {data.get('status')}")

if data.get("status") != "success":
    print(f"Error: {data}")
    sys.exit(1)

result = data.get("result", {})
documents = result.get("documents", [])
download_urls = result.get("files", [])

print(f"Number of sub-documents: {len(documents)}")
print(f"Processing duration:     {result.get('duration_ms', '?')}ms\n")

# Download all split files
headers = {"Authorization": f"Bearer {api_key}"}

for i, doc in enumerate(documents):
    filename = doc.get("suggested_filename", f"part_{i+1}.pdf")
    page_range = doc.get("page_range", "?")
    doc_type = doc.get("document_type", "?")

    print(f"  [{i+1}] {filename}")
    print(f"      Type: {doc_type}, Pages: {page_range}")

    if i < len(download_urls):
        dl_response = requests.get(download_urls[i], headers=headers)
        with open(filename, "wb") as out:
            out.write(dl_response.content)
        print(f"      → Saved as: {filename}")

print(f"\nDone — {len(documents)} files downloaded.")
