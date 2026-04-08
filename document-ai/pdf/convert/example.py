#!/usr/bin/env python3
"""PaperOffice AI — PDF in andere Formate konvertieren"""
import os
import sys
import requests

api_base = "https://api.paperoffice.ai/latest"
api_key = os.environ.get("PAPEROFFICE_API_KEY")
if not api_key:
    sys.exit("Fehler: PAPEROFFICE_API_KEY nicht gesetzt")

input_file = sys.argv[1] if len(sys.argv) > 1 else None
target_format = sys.argv[2] if len(sys.argv) > 2 else "docx"

if not input_file:
    sys.exit("Verwendung: python3 example.py datei.pdf [docx|xlsx|pptx|html|txt|jpg|png]")

# PDF hochladen und konvertieren
with open(input_file, "rb") as f:
    response = requests.post(
        f"{api_base}/job/add/workflow",
        headers={"Authorization": f"Bearer {api_key}"},
        files={"file_1": f},
        data={
            "template": "pdf_convert",
            "target_format": target_format,
            "priority": "900",
        },
    )

data = response.json()
print(f"Status:     {data.get('status')}")
print(f"Zielformat: {target_format}")

if data.get("status") != "success":
    print(f"Fehler: {data}")
    sys.exit(1)

# Konvertierte Datei herunterladen
download_urls = data.get("result", {}).get("files", [])
if not download_urls:
    sys.exit("Fehler: Keine Download-URL erhalten")

output_name = f"ergebnis.{target_format}"
dl_response = requests.get(
    download_urls[0],
    headers={"Authorization": f"Bearer {api_key}"},
)

with open(output_name, "wb") as out:
    out.write(dl_response.content)

print(f"Gespeichert als: {output_name} ({len(dl_response.content)} Bytes)")
