#!/usr/bin/env python3
"""PaperOffice AI — Convert Office documents to PDF (native MS Office)

Pipeline: paperoffice_dataripper___office2pdf
Supported: DOCX, DOC, XLSX, XLS, PPTX, PPT, ODS, ODT, ODP, RTF
Provider: native (Windows VM + real MS Office, best quality)

Always async — native conversion requires a Windows VM.

Usage:
    export PAPEROFFICE_API_KEY=po_sk_xxx
    python3 example.py document.docx [provider]
"""
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
    sys.exit("Usage: python3 example.py <office_file> [provider]")

provider = sys.argv[2] if len(sys.argv) > 2 else "native"
headers = {"Authorization": f"Bearer {api_key}"}


def submit_job(file_path: str, prov: str = "native") -> dict:
    """Submit office2pdf conversion job (always async)."""
    with open(file_path, "rb") as f:
        response = requests.post(
            f"{api_base}/job/add/paperoffice_dataripper___office2pdf",
            headers=headers,
            files=[("files", f)],
            data={"provider": prov, "priority": "500"},
        )
    response.raise_for_status()
    return response.json()


def poll_job(job_id: str, max_attempts: int = 60, initial_interval: int = 5) -> dict:
    """Poll job status until completed or failed."""
    interval = initial_interval
    for attempt in range(1, max_attempts + 1):
        time.sleep(interval)
        response = requests.get(f"{api_base}/job/get/{job_id}", headers=headers)
        data = response.json()
        job_result = data.get("job_result", {})
        status = job_result.get("status", data.get("job_status", "unknown"))

        print(f"  Attempt {attempt}/{max_attempts}: {status}")

        if status == "completed":
            return job_result
        if status in ("failed", "error"):
            raise RuntimeError(f"Job failed: {job_result}")

        if attempt == 5:
            interval = 10

    raise TimeoutError(f"Job not completed after {max_attempts} attempts")


def download_result(job_result: dict, output_path: str):
    """Download converted PDF from job result."""
    result = job_result.get("result", {})
    files = result.get("files", result.get("output_files", []))

    url = None
    if isinstance(files, list) and files:
        entry = files[0]
        if isinstance(entry, dict):
            url = entry.get("download_url") or entry.get("url")
        elif isinstance(entry, str):
            url = entry
    if not url:
        url = result.get("download_url")

    if not url:
        print("Warning: No download URL found in response")
        print(f"Result keys: {list(result.keys())}")
        return

    dl = requests.get(url, headers=headers)
    with open(output_path, "wb") as f:
        f.write(dl.content)
    print(f"Saved as: {output_path} ({len(dl.content)} bytes)")


if __name__ == "__main__":
    print(f">>> Submitting office2pdf: {input_file} (provider: {provider})")
    submit_data = submit_job(input_file, provider)

    if submit_data.get("status") != "success":
        sys.exit(f"Error: {submit_data}")

    job_id = submit_data["job_id"]
    eta = submit_data.get("eta", {})
    print(f"Job submitted: {job_id}")
    print(f"ETA: {eta.get('estimated_completion', '?')} (queue pos: {eta.get('queue_position', '?')})")

    print(">>> Waiting for conversion...")
    job_result = poll_job(job_id)

    output_name = os.path.splitext(input_file)[0] + ".pdf"
    download_result(job_result, output_name)
