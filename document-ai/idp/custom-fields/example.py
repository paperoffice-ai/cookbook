#!/usr/bin/env python3
"""PaperOffice AI — IDP mit eigenen Extraktionsfeldern (Custom Fields)

Definiert eigene Felder zur gezielten Datenextraktion aus beliebigen Dokumenten.

Verwendung:
    export PAPEROFFICE_API_KEY=po_sk_xxx
    python3 example.py vertrag.pdf
"""
import os
import sys
import json
import requests

api_url = "https://api.paperoffice.ai/latest/job/add/workflow"
api_key = os.environ.get("PAPEROFFICE_API_KEY", "")

# Eigene Extraktionsfelder — beliebig anpassbar
custom_fields = [
    {
        "name": "vertragsnummer",
        "type": "string",
        "description": "Vertragsnummer im Dokument",
    },
    {
        "name": "kuendigungsfrist",
        "type": "string",
        "description": "Kündigungsfrist in Monaten oder als Datum",
    },
    {
        "name": "monatlicher_betrag",
        "type": "number",
        "description": "Monatlicher Betrag in Euro",
    },
    {
        "name": "vertragspartner",
        "type": "string",
        "description": "Name des Vertragspartners",
    },
]


def extract_custom_fields(pdf_path: str, fields: list, token: str = api_key) -> dict:
    """Extrahiert eigene Felder aus einem Dokument."""
    if not token:
        raise ValueError("PAPEROFFICE_API_KEY nicht gesetzt")

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
    """Gibt extrahierte Felder als Tabelle aus."""
    pages = data.get("result", {}).get("pages_idp", [])
    if not pages:
        print("Keine IDP-Daten gefunden")
        return

    fields = pages[0].get("suggested_fields", {})
    print(f"Job-ID:  {data.get('job_id', '—')}")
    print(f"Felder:  {len(fields)}")
    print()
    print(f"{'Feld':<28} {'Typ':<10} {'Wert':<40} {'Konfidenz':<10}")
    print("─" * 90)

    for name, info in sorted(fields.items()):
        value = info.get("value", "—")
        field_type = info.get("type", "—")
        confidence = info.get("source_boxes_confidence", "—")
        print(f"{name:<28} {field_type:<10} {value:<40} {confidence:<10}")


if __name__ == "__main__":
    pdf = sys.argv[1] if len(sys.argv) > 1 else None
    if not pdf:
        sys.exit("Verwendung: python3 example.py <datei.pdf>")

    result = extract_custom_fields(pdf, custom_fields)
    print_results(result)
