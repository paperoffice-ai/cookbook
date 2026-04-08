#!/usr/bin/env python3
"""
PaperOffice AI — Vertragsanalyse Pipeline
Verträge → Key Terms Extraktion → Source Box Verification

Verwendung:
    export PAPEROFFICE_API_KEY=po_sk_xxx
    python pipeline.py vertrag.pdf
"""
import os
import sys
import json
import requests

API_URL = "https://api.paperoffice.ai/latest/job/add/workflow"
API_KEY = os.environ.get("PAPEROFFICE_API_KEY", "")


def analyze_contract(pdf_path: str, token: str = API_KEY) -> dict:
    """Extrahiert Key Terms aus einem Vertrag mit Source Boxes."""
    if not token:
        raise ValueError("PAPEROFFICE_API_KEY nicht gesetzt")

    response = requests.post(
        API_URL,
        headers={"Authorization": f"Bearer {token}"},
        files={"file_1": open(pdf_path, "rb")},
        data={
            "model": "premium",
            "idp_collection": "contract",
            "priority": 900,
        },
    )
    response.raise_for_status()

    result = response.json().get("result", {})
    idp_pages = result.get("pages_idp", [])
    if not idp_pages:
        return {}

    fields = idp_pages[0].get("suggested_fields", {})

    key_terms = {}
    for field_name, info in fields.items():
        if info.get("type") == "table":
            continue
        key_terms[field_name] = {
            "value": info.get("value", ""),
            "source_boxes": info.get("source_boxes", []),
            "confidence": info.get("source_boxes_confidence", "low"),
        }

    return key_terms


if __name__ == "__main__":
    pdf = sys.argv[1] if len(sys.argv) > 1 else "vertrag.pdf"
    terms = analyze_contract(pdf)

    if not terms:
        print("Keine Vertragsfelder gefunden")
        sys.exit(1)

    for field, data in terms.items():
        confidence = data.get("confidence", "low")
        marker = "✓" if confidence in ("high", "medium") else "⚠"
        boxes = data.get("source_boxes", [])
        print(f"  {marker} {field}: {data['value']} (confidence: {confidence}, boxes: {len(boxes)})")
