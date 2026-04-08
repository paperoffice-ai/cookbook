#!/usr/bin/env python3
"""PaperOffice AI — DSGVO-konforme Anonymisierung von PDF-Dokumenten"""
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

# Optionale Feldliste (z.B. "name,adresse,iban")
anonymize_fields = sys.argv[2] if len(sys.argv) > 2 else None

# PDF hochladen und anonymisieren
payload = {
    "template": "pdf_anonymize",
    "priority": "900",
}
if anonymize_fields:
    payload["anonymize_fields"] = anonymize_fields

with open(input_file, "rb") as f:
    response = requests.post(
        f"{api_base}/job/add/workflow",
        headers={"Authorization": f"Bearer {api_key}"},
        files={"file_1": f},
        data=payload,
    )

data = response.json()
print(f"Status: {data.get('status')}")

if anonymize_fields:
    print(f"Felder: {anonymize_fields}")

if data.get("status") != "success":
    print(f"Fehler: {data}")
    sys.exit(1)

# Anonymisierte PDF herunterladen
download_urls = data.get("result", {}).get("files", [])
if not download_urls:
    sys.exit("Fehler: Keine Download-URL erhalten")

dl_response = requests.get(
    download_urls[0],
    headers={"Authorization": f"Bearer {api_key}"},
)

with open("anonymisiert.pdf", "wb") as out:
    out.write(dl_response.content)

print(f"Gespeichert als: anonymisiert.pdf ({len(dl_response.content)} Bytes)")
