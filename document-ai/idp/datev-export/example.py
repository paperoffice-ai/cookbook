#!/usr/bin/env python3
"""PaperOffice AI — DATEV Export from Invoice IDP

Extracts invoice data via IDP and converts it into a
DATEV-compatible accounting entry (CSV format).

Usage:
    export PAPEROFFICE_API_KEY=po_ut_xxx
    python3 example.py invoice.pdf
    python3 example.py invoice.pdf > booking.csv
"""
import os
import sys
import csv
import io
import requests

def wait_for_result(data: dict, token: str, api_base: str = "https://api.paperoffice.ai/latest", timeout_s: int = 180) -> dict:
    """HTTP 202 means the job is still running: follow job/get until it is completed."""
    if data.get("result") or not data.get("job_id"):
        return data
    import time
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        time.sleep(2)
        poll = requests.get(f"{api_base}/job/get/{data['job_id']}", headers={"Authorization": f"Bearer {token}"}).json()
        if poll.get("job_status") == "completed" or poll.get("result") or poll.get("job_result"):
            # job/get returns the payload as job_result — expose it under result like the inline response
            if "result" not in poll and "job_result" in poll:
                poll["result"] = poll["job_result"]
            return poll
        if poll.get("job_status") in ("failed", "error") or poll.get("status") == "error":
            raise RuntimeError(f"job failed: {poll.get('message')}")
    raise TimeoutError(f"job {data['job_id']} not finished after {timeout_s}s")


api_url = "https://api.paperoffice.ai/latest/job/add/workflow"
api_key = os.environ.get("PAPEROFFICE_API_KEY", "")

# DATEV chart of accounts SKR04 defaults — customizable
KONTO_KREDITOR = "70000"
KONTO_BANK = "1200"


def extract_invoice(pdf_path: str, token: str = api_key) -> dict:
    """Extracts invoice fields via IDP."""
    if not token:
        raise ValueError("PAPEROFFICE_API_KEY not set")

    with open(pdf_path, "rb") as f:
        response = requests.post(
            api_url,
            headers={"Authorization": f"Bearer {token}"},
            files={"file_1": f},
            data={
                "model": "premium",
                "idp_collection": "invoice",
                "processing_lane": "instant",
            },
        )
    response.raise_for_status()
    return wait_for_result(response.json(), token)


def get_field(fields: dict, name: str, raw: bool = False) -> str:
    """Helper: extract field value from suggested_fields."""
    info = fields.get(name, {})
    if raw:
        return info.get("value_raw", info.get("value", ""))
    return info.get("value", "")


def to_datev_date(iso_date: str) -> str:
    """ISO date (YYYY-MM-DD) → DATEV format (DDMM)."""
    parts = iso_date.split("-")
    if len(parts) == 3:
        return f"{parts[2]}{parts[1]}"
    return ""


def to_datev_csv(fields: dict) -> str:
    """Converts IDP fields to DATEV posting batch CSV."""
    umsatz = get_field(fields, "_total_amount", raw=True)
    datum = get_field(fields, "_invoice_date", raw=True)
    re_nr = get_field(fields, "_invoice_number")
    lieferant = get_field(fields, "_supplier_name")
    ust = get_field(fields, "_vat_rate")

    # Derive BU key from VAT rate
    bu_schluessel = ""
    if ust:
        try:
            rate = float(ust.replace(",", ".").replace("%", ""))
            if rate == 19.0:
                bu_schluessel = "9"
            elif rate == 7.0:
                bu_schluessel = "8"
        except ValueError:
            pass

    datev_header = [
        "Umsatz (ohne Soll/Haben-Kz)",
        "Soll/Haben-Kennzeichen",
        "Konto",
        "Gegenkonto",
        "BU-Schlüssel",
        "Belegdatum",
        "Belegfeld 1",
        "Buchungstext",
    ]

    datev_row = [
        umsatz,
        "S",
        KONTO_KREDITOR,
        KONTO_BANK,
        bu_schluessel,
        to_datev_date(datum),
        re_nr,
        lieferant,
    ]

    output = io.StringIO()
    writer = csv.writer(output, delimiter=";", quoting=csv.QUOTE_MINIMAL)
    writer.writerow(datev_header)
    writer.writerow(datev_row)
    return output.getvalue()


if __name__ == "__main__":
    pdf = sys.argv[1] if len(sys.argv) > 1 else None
    if not pdf:
        sys.exit("Usage: python3 example.py <invoice.pdf>")

    data = extract_invoice(pdf)
    pages = data.get("result", {}).get("pages_idp", [])
    if not pages:
        sys.exit("No IDP data found")

    fields = pages[0].get("suggested_fields", {})

    # Summary of extracted fields
    print("--- Extracted Invoice Data ---")
    print(f"  Invoice no.:  {get_field(fields, '_invoice_number')}")
    print(f"  Date:         {get_field(fields, '_invoice_date')}")
    print(f"  Supplier:     {get_field(fields, '_supplier_name')}")
    print(f"  Amount:       {get_field(fields, '_total_amount')}")
    print(f"  Net:          {get_field(fields, '_net_amount')}")
    print(f"  VAT:          {get_field(fields, '_vat_amount')}")
    print()

    # Generate DATEV CSV
    datev_csv = to_datev_csv(fields)
    print("--- DATEV Accounting Entry (CSV) ---")
    print(datev_csv)
