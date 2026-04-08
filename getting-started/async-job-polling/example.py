#!/usr/bin/env python3
"""PaperOffice AI — Async Job Polling (Submit → Poll → Result)"""
import os
import sys
import time
import requests

api_base = "https://api.paperoffice.ai/latest"
api_key = os.environ.get("PAPEROFFICE_API_KEY")
if not api_key:
    sys.exit("Error: PAPEROFFICE_API_KEY not set")

input_file = sys.argv[1] if len(sys.argv) > 1 else None
if not input_file:
    sys.exit("Error: Please provide file path as argument")

headers = {"Authorization": f"Bearer {api_key}"}

# Step 1: Submit job (priority=500 → async)
print(">>> Submitting job...")
with open(input_file, "rb") as f:
    submit_response = requests.post(
        f"{api_base}/job/add/paperoffice_aiocr___generate",
        headers=headers,
        files={"file_1": f},
        data={"ocr_mode": "text", "priority": "500"},
    )

submit_data = submit_response.json()
job_id = submit_data.get("job_id")
if not job_id:
    sys.exit(f"Error: No job_id received — {submit_data}")

print(f"Job submitted: {job_id}")

# Step 2: Poll status until completed
print(">>> Waiting for result...")
max_attempts = 30

for attempt in range(1, max_attempts + 1):
    time.sleep(2)

    poll_response = requests.get(
        f"{api_base}/job/get/{job_id}",
        headers=headers,
    )
    poll_data = poll_response.json()
    status = poll_data.get("status", "unknown")

    print(f"  Attempt {attempt}/{max_attempts}: {status}")

    if status == "completed":
        result = poll_data.get("result", {})
        output = result.get("output", {})
        summary = output.get("summary", {})
        print()
        print("--- Result ---")
        print(f"Pages: {summary.get('total_pages')}")
        print(f"Lines: {summary.get('total_lines')}")
        print(summary.get("poaiocr_extracted_fulltext", "No text"))
        sys.exit(0)

    if status in ("failed", "error"):
        sys.exit(f"Job failed: {poll_data}")

print(f"Timeout: Job not completed after {max_attempts} attempts")
sys.exit(1)
