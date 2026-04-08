#!/usr/bin/env python3
"""PaperOffice AI — OCR Complete-Mode (text + bounding boxes + tables)"""
import os
import sys
import json
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
        data={"ocr_mode": "complete", "priority": "900"},
    )

data = response.json()
result = data.get("result", {})
output = result.get("output", {})
summary = output.get("summary", {})
pages = output.get("pages", {})

print(f"Status:     {data.get('status')}")
print(f"Pages:      {summary.get('total_pages')}")
print(f"Lines:      {summary.get('total_lines')}")
print(f"Characters: {summary.get('total_chars')}")
print(f"Confidence: {summary.get('avg_confidence')}")
print(f"Duration:   {result.get('duration_ms')} ms")
print()

for page_id, page_data in sorted(pages.items()):
    print(f"=== Page {page_id} ===")
    print(f"  Text lines:     {page_data.get('line_count')}")
    print(f"  Confidence:     {page_data.get('confidence_avg')}")
    print(f"  Language:       {page_data.get('language', {}).get('primary')}")

    bboxes = page_data.get("bounding_boxes")
    if bboxes:
        print(f"  Bounding Boxes: {len(bboxes)} elements")
        for i, box in enumerate(bboxes[:3]):
            print(f"    [{i}] text={box.get('text', '')[:50]!r}  "
                  f"pos=({box.get('x')},{box.get('y')},{box.get('w')},{box.get('h')})")
        if len(bboxes) > 3:
            print(f"    ... and {len(bboxes) - 3} more")

    tables = page_data.get("tables")
    if tables:
        print(f"  Tables:         {len(tables)} detected")
        for i, table in enumerate(tables):
            rows = table.get("rows", [])
            print(f"    Table {i}: {len(rows)} rows")

    print()

print("--- Full text ---")
print(summary.get("poaiocr_extracted_fulltext", "No text extracted"))
