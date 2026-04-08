#!/usr/bin/env python3
"""PaperOffice AI — Generate searchable PDF (OCR + Searchable PDF)"""
import os
import sys
import requests

api_base = "https://api.paperoffice.ai/latest"
api_key = os.environ.get("PAPEROFFICE_API_KEY")
if not api_key:
    sys.exit("Error: PAPEROFFICE_API_KEY not set")

input_file = sys.argv[1] if len(sys.argv) > 1 else None
if not input_file:
    sys.exit("Error: Please provide file path as argument")

output_file = sys.argv[2] if len(sys.argv) > 2 else "searchable_output.pdf"
headers = {"Authorization": f"Bearer {api_key}"}

with open(input_file, "rb") as f:
    response = requests.post(
        f"{api_base}/job/add/paperoffice_aiocr___generate",
        headers=headers,
        files={"file_1": f},
        data={
            "ocr_mode": "text",
            "output_searchable_pdf": "true",
            "priority": "900",
        },
    )

data = response.json()
result = data.get("result", {})
output = result.get("output", {})
summary = output.get("summary", {})

print(f"Status:     {data.get('status')}")
print(f"Pages:      {summary.get('total_pages')}")
print(f"Confidence: {summary.get('avg_confidence')}")
print(f"Duration:   {result.get('duration_ms')} ms")

# Download searchable PDF
pdf_url = output.get("searchable_pdf_url") or output.get("download_url")
download_token = output.get("download_token")

if pdf_url:
    print(f"PDF download: {pdf_url}")
    pdf_response = requests.get(pdf_url, headers=headers)
    with open(output_file, "wb") as out:
        out.write(pdf_response.content)
    print(f"Saved: {output_file} ({len(pdf_response.content)} bytes)")
elif download_token:
    print(f"Download token: {download_token}")
    pdf_response = requests.get(
        f"{api_base}/job/download/{download_token}",
        headers=headers,
    )
    with open(output_file, "wb") as out:
        out.write(pdf_response.content)
    print(f"Saved: {output_file} ({len(pdf_response.content)} bytes)")
else:
    print("No PDF download found in the response.")
    print("Full response:")
    import json
    print(json.dumps(data, indent=2, ensure_ascii=False))
