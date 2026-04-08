#!/usr/bin/env python3
"""PaperOffice AI — Intelligentes PDF-Splitting mit KI-Erkennung"""
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

# PDF hochladen und KI-basiert splitten
with open(input_file, "rb") as f:
    response = requests.post(
        f"{api_base}/job/add/workflow",
        headers={"Authorization": f"Bearer {api_key}"},
        files={"file_1": f},
        data={
            "template": "pdf_ai_split",
            "naming_instruction": "Benenne nach Dokumenttyp und Datum",
            "priority": "900",
        },
    )

data = response.json()
print(f"Status: {data.get('status')}")

if data.get("status") != "success":
    print(f"Fehler: {data}")
    sys.exit(1)

result = data.get("result", {})
documents = result.get("documents", [])
download_urls = result.get("files", [])

print(f"Anzahl Teildokumente: {len(documents)}")
print(f"Verarbeitungsdauer:   {result.get('duration_ms', '?')}ms\n")

# Alle gesplitteten Dateien herunterladen
headers = {"Authorization": f"Bearer {api_key}"}

for i, doc in enumerate(documents):
    filename = doc.get("suggested_filename", f"teil_{i+1}.pdf")
    page_range = doc.get("page_range", "?")
    doc_type = doc.get("document_type", "?")

    print(f"  [{i+1}] {filename}")
    print(f"      Typ: {doc_type}, Seiten: {page_range}")

    if i < len(download_urls):
        dl_response = requests.get(download_urls[i], headers=headers)
        with open(filename, "wb") as out:
            out.write(dl_response.content)
        print(f"      → Gespeichert als: {filename}")

print(f"\nFertig — {len(documents)} Dateien heruntergeladen.")
