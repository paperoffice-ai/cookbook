#!/usr/bin/env python3
"""PaperOffice AI — Vertragsanalyse (IDP Contract)

Extrahiert Vertragsparteien, Laufzeit, Kündigungsfrist und mehr.

Verwendung:
    export PAPEROFFICE_API_KEY=po_sk_xxx
    python3 example.py vertrag.pdf
"""
import os
import sys
import requests

api_url = "https://api.paperoffice.ai/latest/job/add/workflow"
api_key = os.environ.get("PAPEROFFICE_API_KEY", "")


def extract_contract(pdf_path: str, token: str = api_key) -> dict:
    """Extrahiert Vertragsfelder via IDP."""
    if not token:
        raise ValueError("PAPEROFFICE_API_KEY nicht gesetzt")

    with open(pdf_path, "rb") as f:
        response = requests.post(
            api_url,
            headers={"Authorization": f"Bearer {token}"},
            files={"file_1": f},
            data={
                "model": "premium",
                "idp_collection": "contract",
                "priority": 900,
            },
        )
    response.raise_for_status()
    return response.json()


def print_contract(data: dict):
    """Gibt Vertragsfelder formatiert aus."""
    pages = data.get("result", {}).get("pages_idp", [])
    if not pages:
        print("Keine IDP-Daten gefunden")
        return

    fields = pages[0].get("suggested_fields", {})
    print(f"Job-ID:  {data.get('job_id', '—')}")
    print(f"Felder:  {len(fields)}")
    print()
    print(f"{'Feld':<32} {'Wert':<42} {'Konfidenz':<10}")
    print("─" * 86)

    for name, info in sorted(fields.items()):
        if info.get("type") == "table":
            continue
        value = info.get("value", "—")
        confidence = info.get("source_boxes_confidence", "—")
        print(f"{name:<32} {value:<42} {confidence:<10}")


if __name__ == "__main__":
    pdf = sys.argv[1] if len(sys.argv) > 1 else None
    if not pdf:
        sys.exit("Verwendung: python3 example.py <vertrag.pdf>")

    result = extract_contract(pdf)
    print_contract(result)
