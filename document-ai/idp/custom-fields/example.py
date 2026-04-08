#!/usr/bin/env python3
"""PaperOffice AI — IDP with Custom Extraction Fields (Custom Fields)

Defines custom fields for targeted data extraction from any document.

Usage:
    export PAPEROFFICE_API_KEY=po_sk_xxx
    python3 example.py contract.pdf
"""
import os
import sys
import json
import requests

api_url = "https://api.paperoffice.ai/latest/job/add/workflow"
api_key = os.environ.get("PAPEROFFICE_API_KEY", "")

# Custom extraction fields — freely customizable
custom_fields = [
    {
        "name": "vertragsnummer",
        "type": "string",
        "description": "Contract number in the document",
    },
    {
        "name": "kuendigungsfrist",
        "type": "string",
        "description": "Cancellation period in months or as a date",
    },
    {
        "name": "monatlicher_betrag",
        "type": "number",
        "description": "Monthly amount in euros",
    },
    {
        "name": "vertragspartner",
        "type": "string",
        "description": "Name of the contracting party",
    },
]


def extract_custom_fields(pdf_path: str, fields: list, token: str = api_key) -> dict:
    """Extracts custom fields from a document."""
    if not token:
        raise ValueError("PAPEROFFICE_API_KEY not set")

    with open(pdf_path, "rb") as f:
        response = requests.post(
            api_url,
            headers={"Authorization": f"Bearer {token}"},
            files={"file_1": f},
            data={
                "model": "premium",
                "idp_fields": json.dumps(fields),
                "priority": 900,
            },
        )
    response.raise_for_status()
    return response.json()


def print_results(data: dict):
    """Prints extracted fields as a table."""
    pages = data.get("result", {}).get("pages_idp", [])
    if not pages:
        print("No IDP data found")
        return

    fields = pages[0].get("suggested_fields", {})
    print(f"Job ID:  {data.get('job_id', '—')}")
    print(f"Fields:  {len(fields)}")
    print()
    print(f"{'Field':<28} {'Type':<10} {'Value':<40} {'Confidence':<10}")
    print("─" * 90)

    if isinstance(fields, dict):
        items = sorted(fields.items())
    elif isinstance(fields, list):
        items = [(f.get("name") or f.get("label", "—"), f) for f in fields]
    else:
        items = []

    for name, info in items:
        value = info.get("value", "—")
        field_type = info.get("type", "—")
        confidence = info.get("source_boxes_confidence", info.get("confidence", "—"))
        print(f"{name:<28} {field_type:<10} {value:<40} {confidence:<10}")


if __name__ == "__main__":
    pdf = sys.argv[1] if len(sys.argv) > 1 else None
    if not pdf:
        sys.exit("Usage: python3 example.py <file.pdf>")

    result = extract_custom_fields(pdf, custom_fields)
    print_results(result)
