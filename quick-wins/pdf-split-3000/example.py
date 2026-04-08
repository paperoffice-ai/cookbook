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
import requests

API_URL = "https://api.paperoffice.ai/latest/job"
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
    result = split_pdf(pdf)

    docs = result.get("job_result", {}).get("documents_created", [])
    for doc in docs:
        print(f"{doc['suggested_filename']}: Seiten {doc['page_range']}")
