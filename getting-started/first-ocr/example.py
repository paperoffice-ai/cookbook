#!/usr/bin/env python3
"""PaperOffice AI — Erster OCR-Call (Text-Extraktion)"""
import os
import sys
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
        data={"ocr_mode": "text", "priority": "900"},
    )

data = response.json()
result = data.get("result", {})
output = result.get("output", {})
summary = output.get("summary", {})

print(f"Seiten: {summary.get('total_pages')}")
print(f"Zeilen: {summary.get('total_lines')}")
print(f"Konfidenz: {summary.get('avg_confidence')}")
print()
print("--- Extrahierter Text ---")
print(summary.get("poaiocr_extracted_fulltext", "Kein Text extrahiert"))
