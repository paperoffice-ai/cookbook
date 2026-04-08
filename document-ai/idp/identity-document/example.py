#!/usr/bin/env python3
"""PaperOffice AI — Identity Document Extraction (IDP Identity)

Extracts data from ID cards, passports, or driver's licenses.

Usage:
    export PAPEROFFICE_API_KEY=po_sk_xxx
    python3 example.py id_card.pdf
"""
import os
import sys
import requests

api_url = "https://api.paperoffice.ai/latest/job/add/workflow"
api_key = os.environ.get("PAPEROFFICE_API_KEY", "")


def extract_identity(file_path: str, token: str = api_key) -> dict:
    """Extracts identity document data via IDP."""
    if not token:
        raise ValueError("PAPEROFFICE_API_KEY not set")

    with open(file_path, "rb") as f:
        response = requests.post(
            api_url,
            headers={"Authorization": f"Bearer {token}"},
            files={"file_1": f},
            data={
                "model": "premium",
                "idp_collection": "identity_document",
                "priority": 900,
            },
        )
    response.raise_for_status()
    return response.json()


def print_identity(data: dict):
    """Prints identity document fields in formatted output."""
    pages = data.get("result", {}).get("pages_idp", [])
    if not pages:
        print("No IDP data found")
        return

    fields = pages[0].get("suggested_fields", {})
    print(f"Job ID:  {data.get('job_id', '—')}")
    print(f"Fields:  {len(fields)}")
    print()
    print(f"{'Field':<32} {'Value':<42} {'Confidence':<10}")
    print("─" * 86)

    for name, info in sorted(fields.items()):
        value = info.get("value", "—")
        confidence = info.get("source_boxes_confidence", "—")
        print(f"{name:<32} {value:<42} {confidence:<10}")


if __name__ == "__main__":
    pdf = sys.argv[1] if len(sys.argv) > 1 else None
    if not pdf:
        sys.exit("Usage: python3 example.py <id_card.pdf>")

    result = extract_identity(pdf)
    print_identity(result)
