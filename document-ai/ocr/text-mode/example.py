#!/usr/bin/env python3
"""PaperOffice AI — OCR Text-Mode (plain text only, fastest mode)"""
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

with open(input_file, "rb") as f:
    response = requests.post(
        f"{api_base}/job/add/paperoffice_aiocr___generate",
        headers={"Authorization": f"Bearer {api_key}"},
        files={"file_1": f},
        data={"ocr_mode": "text", "priority": "900"},
    )

data = response.json()
result = data.get("result", {})
output = result.get("output", {})
summary = output.get("summary", {})

print(f"Status:     {data.get('status')}")
print(f"Pages:      {summary.get('total_pages')}")
print(f"Lines:      {summary.get('total_lines')}")
print(f"Characters: {summary.get('total_chars')}")
print(f"Confidence: {summary.get('avg_confidence')}")
print(f"Engine:     {summary.get('processing_engine')}")
print()
print("--- Extracted text ---")
print(summary.get("poaiocr_extracted_fulltext", "No text extracted"))
