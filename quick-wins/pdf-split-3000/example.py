#!/usr/bin/env python3
"""
PaperOffice AI — AI PDF Split (bis 3000 Seiten)
Bearer Token ERFORDERLICH

Verwendung:
    export PAPEROFFICE_API_KEY=po_sk_xxx
    python example.py sammel_dokument.pdf
"""
import os
import sys
import json
import requests

API_URL = "https://api.paperoffice.ai/latest/job/add/workflow"
API_KEY = os.environ.get("PAPEROFFICE_API_KEY", "")


def split_pdf(pdf_path: str, locale: str = "de_DE", token: str = API_KEY) -> dict:
    """Splittet ein Sammel-PDF anhand von AI-erkannten Dokumentgrenzen."""
    if not token:
        raise ValueError("PAPEROFFICE_API_KEY nicht gesetzt")

    response = requests.post(
        API_URL,
        headers={"Authorization": f"Bearer {token}"},
        files={"file": open(pdf_path, "rb")},
        data={
            "template": "pdf_ai_split",
            "naming_instruction": "Dokumenttyp_Datum_Absender",
            "locale": locale,
            "priority": 900,
        },
    )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    pdf = sys.argv[1] if len(sys.argv) > 1 else "sammel_dokument.pdf"
    data = split_pdf(pdf)

    if data.get("status") != "success":
        print(f"Fehler: {data.get('message', 'Unbekannt')}")
        sys.exit(1)

    result = data.get("result", {})
    print(f"Status: {data['status']}")
    print(f"Schritte: {result.get('total_steps', 'N/A')}")
    print(f"Dauer: {result.get('duration_ms', 'N/A')}ms")
    print(json.dumps(result, indent=2, ensure_ascii=False))
