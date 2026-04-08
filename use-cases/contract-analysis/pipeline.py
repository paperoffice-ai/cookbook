#!/usr/bin/env python3
"""
PaperOffice AI — Vertragsanalyse Pipeline
Verträge → Key Terms Extraktion → Bounding Box Verification

Verwendung:
    export PAPEROFFICE_API_KEY=po_sk_xxx
    python pipeline.py vertrag.pdf
"""
import os
import sys
import requests

API_URL = "https://api.paperoffice.ai/latest/job"
API_KEY = os.environ.get("PAPEROFFICE_API_KEY", "")


def analyze_contract(pdf_path: str, token: str = API_KEY) -> dict:
    """Extrahiert Key Terms aus einem Vertrag mit Bounding Boxes."""
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

    contract = response.json().get("job_result", {})
    fields = contract.get("fields", {})

    key_terms = {}
    target_fields = ["parties", "start_date", "end_date", "notice_period"]

    for field_name in target_fields:
        if field_name in fields:
            data = fields[field_name]
            key_terms[field_name] = {
                "value": data.get("value", ""),
                "bbox": data.get("bbox", []),
                "confidence": data.get("confidence", 0),
            }

    return key_terms


if __name__ == "__main__":
    pdf = sys.argv[1] if len(sys.argv) > 1 else "vertrag.pdf"
    terms = analyze_contract(pdf)

    for field, data in terms.items():
        confidence = data.get("confidence", 0)
        marker = "✓" if confidence >= 0.9 else "⚠"
        print(f"  {marker} {field}: {data['value']} @ bbox {data['bbox']}")
