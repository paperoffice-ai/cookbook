#!/usr/bin/env python3
"""
PaperOffice AI — Batch OCR → CSV Export
Ordner mit Dokumenten → OCR → CSV

Verwendung:
    export PAPEROFFICE_API_KEY=po_sk_xxx
    python pipeline.py ./documents ocr_results.csv
"""
import os
import sys
import csv
from pathlib import Path
import requests

API_URL = "https://api.paperoffice.ai/latest/job"
API_KEY = os.environ.get("PAPEROFFICE_API_KEY", "")

SUPPORTED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg", ".tiff", ".webp"}


def batch_ocr_to_csv(
    folder_path: str, output_csv: str = "ocr_results.csv", token: str = API_KEY
) -> list[dict]:
    """Verarbeitet alle Dokumente in einem Ordner und exportiert nach CSV."""
    if not token:
        raise ValueError("PAPEROFFICE_API_KEY nicht gesetzt")

    headers = {"Authorization": f"Bearer {token}"}

    files = [
        f
        for f in Path(folder_path).iterdir()
        if f.suffix.lower() in SUPPORTED_EXTENSIONS
    ]

    if not files:
        print(f"Keine unterstützten Dateien in: {folder_path}")
        return []

    results = []
    for file_path in files:
        print(f"→ Verarbeite: {file_path.name}")
        try:
            response = requests.post(
                API_URL,
                headers=headers,
                files={"file_1": open(file_path, "rb")},
                data={"ocr_mode": "complete", "priority": 900},
            )
            response.raise_for_status()
            result = response.json().get("job_result", {})

            results.append(
                {
                    "filename": file_path.name,
                    "pages": result.get("page_count", 1),
                    "text_length": len(result.get("text", "")),
                    "text_preview": result.get("text", "")[:500],
                    "confidence": result.get("confidence", 0),
                }
            )
        except Exception as e:
            print(f"  ✗ Fehler: {e}")

    if results:
        with open(output_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
        print(f"\n✓ {len(results)} Dokumente → {output_csv}")

    return results


if __name__ == "__main__":
    folder = sys.argv[1] if len(sys.argv) > 1 else "."
    output = sys.argv[2] if len(sys.argv) > 2 else "ocr_results.csv"
    batch_ocr_to_csv(folder, output)
