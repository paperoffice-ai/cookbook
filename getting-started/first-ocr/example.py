#!/usr/bin/env python3
"""PaperOffice AI — First OCR Call (Text Extraction)"""
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

with open(input_file, "rb") as f:
    response = requests.post(
        f"{api_base}/job/add/paperoffice_aiocr___generate",
        headers={"Authorization": f"Bearer {api_key}"},
        files={"file_1": f},
        data={"ocr_mode": "text", "processing_lane": "instant"},
    )

data = wait_for_result(response.json(), api_key)
result = data.get("result", {})
output = result.get("output", {})
summary = output.get("summary", {})

print(f"Pages: {summary.get('total_pages')}")
print(f"Lines: {summary.get('total_lines')}")
print(f"Confidence: {summary.get('avg_confidence')}")
print()
print("--- Extracted Text ---")
print(summary.get("poaiocr_extracted_fulltext", "No text extracted"))
