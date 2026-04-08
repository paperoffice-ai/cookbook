#!/usr/bin/env python3
"""PaperOffice AI — OCR Complete-Mode (Text + Bounding Boxes + Tabellen)"""
import os
import sys
import json
import requests

api_base = "https://api.paperoffice.ai/latest"
api_key = os.environ.get("PAPEROFFICE_API_KEY")
if not api_key:
    sys.exit("Fehler: PAPEROFFICE_API_KEY nicht gesetzt")

input_file = sys.argv[1] if len(sys.argv) > 1 else None
if not input_file:
    sys.exit("Fehler: Dateipfad als Argument übergeben")

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

print(f"Status:    {data.get('status')}")
print(f"Seiten:    {summary.get('total_pages')}")
print(f"Zeilen:    {summary.get('total_lines')}")
print(f"Zeichen:   {summary.get('total_chars')}")
print(f"Konfidenz: {summary.get('avg_confidence')}")
print(f"Dauer:     {result.get('duration_ms')} ms")
print()

for page_id, page_data in sorted(pages.items()):
    print(f"=== Seite {page_id} ===")
    print(f"  Text-Zeilen:    {page_data.get('line_count')}")
    print(f"  Konfidenz:      {page_data.get('confidence_avg')}")
    print(f"  Sprache:        {page_data.get('language', {}).get('primary')}")

    bboxes = page_data.get("bounding_boxes")
    if bboxes:
        print(f"  Bounding Boxes: {len(bboxes)} Elemente")
        for i, box in enumerate(bboxes[:3]):
            print(f"    [{i}] text={box.get('text', '')[:50]!r}  "
                  f"pos=({box.get('x')},{box.get('y')},{box.get('w')},{box.get('h')})")
        if len(bboxes) > 3:
            print(f"    ... und {len(bboxes) - 3} weitere")

    tables = page_data.get("tables")
    if tables:
        print(f"  Tabellen:       {len(tables)} erkannt")
        for i, table in enumerate(tables):
            rows = table.get("rows", [])
            print(f"    Tabelle {i}: {len(rows)} Zeilen")

    print()

print("--- Volltext ---")
print(summary.get("poaiocr_extracted_fulltext", "Kein Text extrahiert"))
