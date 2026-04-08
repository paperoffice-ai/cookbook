#!/usr/bin/env python3
"""
PaperOffice AI — Kreditorenbuchhaltung (Accounts Payable Automation)
Eingangsrechnungen → Extraktion → Validation → Export

Verwendung:
    export PAPEROFFICE_API_KEY=po_sk_xxx
    python pipeline.py invoice.pdf
    python pipeline.py ./rechnungen/  # ganzer Ordner
"""
import os
import sys
import csv
from pathlib import Path
import requests

API_URL = "https://api.paperoffice.ai/latest/job/add/workflow"
API_KEY = os.environ.get("PAPEROFFICE_API_KEY", "")


def process_invoice(pdf_path: str, token: str = API_KEY) -> dict:
    """Extrahiert Rechnungsfelder mit Source Boxes für Verification."""
    if not token:
        raise ValueError("PAPEROFFICE_API_KEY nicht gesetzt")

    response = requests.post(
        API_URL,
        headers={"Authorization": f"Bearer {token}"},
        files={"file_1": open(pdf_path, "rb")},
        data={
            "model": "premium",
            "idp_collection": "invoice",
            "priority": 900,
        },
    )
    response.raise_for_status()

    result = response.json().get("result", {})
    idp_pages = result.get("pages_idp", [])
    if not idp_pages:
        return {}

    fields = idp_pages[0].get("suggested_fields", {})

    for field_name, info in fields.items():
        if info.get("type") == "table":
            continue
        confidence = info.get("source_boxes_confidence", "low")
        if confidence == "low":
            boxes = info.get("source_boxes", [])
            print(f"  ⚠ Review nötig: {field_name} (confidence: {confidence}, boxes: {len(boxes)})")

    return {
        "supplier": fields.get("_supplier_name", {}).get("value", ""),
        "amount": fields.get("_total_amount", {}).get("value", ""),
        "date": fields.get("_invoice_date", {}).get("value", ""),
        "iban": fields.get("_creditor_iban", {}).get("value", ""),
        "invoice_number": fields.get("_invoice_number", {}).get("value", ""),
    }


def process_folder(folder_path: str, output_csv: str = "invoices.csv"):
    """Verarbeitet alle PDFs in einem Ordner und exportiert nach CSV."""
    pdf_files = list(Path(folder_path).glob("*.pdf"))
    if not pdf_files:
        print(f"Keine PDFs gefunden in: {folder_path}")
        return

    results = []
    for pdf in pdf_files:
        print(f"→ Verarbeite: {pdf.name}")
        try:
            data = process_invoice(str(pdf))
            data["filename"] = pdf.name
            results.append(data)
        except Exception as e:
            print(f"  ✗ Fehler: {e}")

    if results:
        with open(output_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
        print(f"\n✓ {len(results)} Rechnungen → {output_csv}")


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    path = Path(target)

    if path.is_dir():
        process_folder(str(path))
    elif path.is_file():
        result = process_invoice(str(path))
        for k, v in result.items():
            print(f"  {k}: {v}")
    else:
        print(f"Nicht gefunden: {target}")
