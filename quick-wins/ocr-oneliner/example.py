#!/usr/bin/env python3
"""
PaperOffice AI — OCR One-Liner
Bearer Token ERFORDERLICH

Verwendung:
    export PAPEROFFICE_API_KEY=po_sk_xxx
    python example.py document.png
"""
import os
import sys
import requests

API_URL = "https://api.paperoffice.ai/latest/job/add/workflow"
API_KEY = os.environ.get("PAPEROFFICE_API_KEY", "")


def ocr(file_path: str, mode: str = "complete", token: str = API_KEY) -> dict:
    """
    OCR mit wählbarem Modus.
    mode: 'complete' (Text+Tabellen), 'grid' (nur Bounding Boxes), 'text' (nur Text)
    """
    if not token:
        raise ValueError("PAPEROFFICE_API_KEY nicht gesetzt")

    response = requests.post(
        API_URL,
        headers={"Authorization": f"Bearer {token}"},
        files={"file_1": open(file_path, "rb")},
        data={"ocr_mode": mode, "priority": 900},
    )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    file = sys.argv[1] if len(sys.argv) > 1 else "document.png"
    result = ocr(file)
    print(result.get("result", {}).get("fulltext", ""))
