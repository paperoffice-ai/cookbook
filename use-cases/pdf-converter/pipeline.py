#!/usr/bin/env python3
"""
PaperOffice AI — PDF Converter
PDF → Word, PowerPoint, PDF/A, WebP

Verwendung:
    export PAPEROFFICE_API_KEY=po_sk_xxx
    python pipeline.py report.pdf word
    python pipeline.py contract.pdf pdfa
"""
import os
import sys
import json
import requests

API_URL = "https://api.paperoffice.ai/latest/job/add/workflow"
API_KEY = os.environ.get("PAPEROFFICE_API_KEY", "")

VALID_FORMATS = {"word", "powerpoint", "pdfa", "webp"}


def convert_pdf(
    pdf_path: str, target_format: str, token: str = API_KEY
) -> dict:
    """
    Konvertiert PDF in ein anderes Format.
    target_format: 'word', 'powerpoint', 'pdfa', 'webp'
    """
    if not token:
        raise ValueError("PAPEROFFICE_API_KEY nicht gesetzt")

    if target_format not in VALID_FORMATS:
        raise ValueError(f"Ungültiges Format: {target_format}. Erlaubt: {VALID_FORMATS}")

    response = requests.post(
        API_URL,
        headers={"Authorization": f"Bearer {token}"},
        files={"file_1": open(pdf_path, "rb")},
        data={
            "target_format": target_format,
            "priority": 900,
        },
    )
    response.raise_for_status()

    data = response.json()
    if data.get("status") != "success":
        print(f"Fehler: {data.get('message', 'Unbekannt')}")
        return data

    result = data.get("result", {})
    print(f"Status: {data['status']}")
    print(f"Dauer: {result.get('duration_ms', 'N/A')}ms")
    return data


if __name__ == "__main__":
    pdf = sys.argv[1] if len(sys.argv) > 1 else "report.pdf"
    fmt = sys.argv[2] if len(sys.argv) > 2 else "word"

    data = convert_pdf(pdf, fmt)
    print(json.dumps(data.get("result", {}), indent=2, ensure_ascii=False))
