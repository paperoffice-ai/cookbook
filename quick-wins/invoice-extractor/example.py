#!/usr/bin/env python3
"""
PaperOffice AI — Invoice Extractor mit Bounding Boxes
Bearer Token ERFORDERLICH

Verwendung:
    export PAPEROFFICE_API_KEY=po_sk_xxx
    python example.py invoice.pdf
"""
import os
import sys
import requests

API_URL = "https://api.paperoffice.ai/latest/job/add/workflow"
API_KEY = os.environ.get("PAPEROFFICE_API_KEY", "")


def extract_invoice(pdf_path: str, token: str = API_KEY) -> dict:
    """Extrahiert Rechnungsfelder inkl. Source Boxes via IDP."""
    if not token:
        raise ValueError("PAPEROFFICE_API_KEY nicht gesetzt")

    response = requests.post(
        API_URL,
        headers={"Authorization": f"Bearer {token}"},
        files={"file_1": open(pdf_path, "rb")},
        data={
            "model": "premium",
            "idp_collection": "invoice",
            "priority": 900,
        },
    )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    pdf = sys.argv[1] if len(sys.argv) > 1 else "invoice.pdf"
    data = extract_invoice(pdf)

    idp_pages = data.get("result", {}).get("pages_idp", [])
    if not idp_pages:
        print("Keine IDP-Daten gefunden")
        sys.exit(1)

    fields = idp_pages[0].get("suggested_fields", {})
    for field_name, info in fields.items():
        if info.get("type") == "table":
            continue
        value = info.get("value", "")
        boxes = info.get("source_boxes", [])
        print(f"{field_name}: {value} (source_boxes: {len(boxes)})")
