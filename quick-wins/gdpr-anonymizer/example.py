#!/usr/bin/env python3
"""
PaperOffice AI — DSGVO Anonymisierung (PII Preview)
Bearer Token ERFORDERLICH

Verwendung:
    export PAPEROFFICE_API_KEY=po_sk_xxx
    python example.py dokument.pdf
"""
import os
import sys
import requests

API_URL = "https://api.paperoffice.ai/latest/job/add/workflow"
API_KEY = os.environ.get("PAPEROFFICE_API_KEY", "")


def anonymize_preview(
    file_path: str,
    categories: str = "all",
    whitelist: str | None = None,
    token: str = API_KEY,
) -> dict:
    """
    Erkennt personenbezogene Daten (PII) und gibt deren Positionen zurück.
    categories: 'all' oder kommagetrennt: 'names,addresses,iban'
    whitelist: Begriffe die NICHT geschwärzt werden sollen
    """
    if not token:
        raise ValueError("PAPEROFFICE_API_KEY nicht gesetzt")

    data = {
        "template": "document_anonymize_preview",
        "redact_categories": categories,
        "priority": 900,
    }
    if whitelist:
        data["whitelist"] = whitelist

    response = requests.post(
        API_URL,
        headers={"Authorization": f"Bearer {token}"},
        files={"file": open(file_path, "rb")},
        data=data,
    )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    file = sys.argv[1] if len(sys.argv) > 1 else "dokument.pdf"
    data = anonymize_preview(file, whitelist="PaperOffice")

    result = data.get("result", {})
    boxes = result.get("simplified_boxes", [])
    pii = result.get("detected_pii", {})
    redacted = pii.get("redact_box_ids", [])

    print(f"Gefunden: {len(boxes)} sensible Elemente")
    print(f"Zum Schwärzen markiert: {len(redacted)}")
    for box in boxes:
        print(f"  → {box}")
