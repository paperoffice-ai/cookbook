#!/usr/bin/env python3
"""PaperOffice AI — Mehrere PDFs zu einem Dokument zusammenfügen"""
import os
import sys
import requests

api_base = "https://api.paperoffice.ai/latest"
api_key = os.environ.get("PAPEROFFICE_API_KEY")
if not api_key:
    sys.exit("Fehler: PAPEROFFICE_API_KEY nicht gesetzt")

if len(sys.argv) < 3:
    sys.exit("Fehler: Mindestens 2 PDF-Dateien als Argumente übergeben")

input_files = sys.argv[1:]

# Alle PDFs als file_1, file_2, ... hochladen
files_payload = {}
for i, path in enumerate(input_files, 1):
    files_payload[f"file_{i}"] = open(path, "rb")

try:
    response = requests.post(
        f"{api_base}/job/add/workflow",
        headers={"Authorization": f"Bearer {api_key}"},
        files=files_payload,
        data={
            "template": "pdf_merge",
            "output_filename": "merged.pdf",
            "priority": "900",
        },
    )
finally:
    for fh in files_payload.values():
        fh.close()

data = response.json()
print(f"Status: {data.get('status')}")
print(f"Zusammengefügt: {len(input_files)} Dateien")

if data.get("status") != "success":
    print(f"Fehler: {data}")
    sys.exit(1)

# Zusammengefügtes PDF herunterladen
download_urls = data.get("result", {}).get("files", [])
if not download_urls:
    sys.exit("Fehler: Keine Download-URL erhalten")

dl_response = requests.get(
    download_urls[0],
    headers={"Authorization": f"Bearer {api_key}"},
)

with open("merged.pdf", "wb") as out:
    out.write(dl_response.content)

print(f"Gespeichert als: merged.pdf ({len(dl_response.content)} Bytes)")
