#!/usr/bin/env python3
"""PaperOffice AI — DATEV-Export aus Rechnungs-IDP

Extrahiert Rechnungsdaten via IDP und konvertiert sie in einen
DATEV-kompatiblen Buchungssatz (CSV-Format).

Verwendung:
    export PAPEROFFICE_API_KEY=po_sk_xxx
    python3 example.py rechnung.pdf
    python3 example.py rechnung.pdf > buchung.csv
"""
import os
import sys
import csv
import io
import requests

api_url = "https://api.paperoffice.ai/latest/job/add/workflow"
api_key = os.environ.get("PAPEROFFICE_API_KEY", "")

# DATEV Kontenrahmen SKR04 Defaults — anpassbar
KONTO_KREDITOR = "70000"
KONTO_BANK = "1200"


def extract_invoice(pdf_path: str, token: str = api_key) -> dict:
    """Extrahiert Rechnungsfelder via IDP."""
    if not token:
        raise ValueError("PAPEROFFICE_API_KEY nicht gesetzt")

    with open(pdf_path, "rb") as f:
        response = requests.post(
            api_url,
            headers={"Authorization": f"Bearer {token}"},
            files={"file_1": f},
            data={
                "model": "premium",
                "idp_collection": "invoice",
                "priority": 900,
            },
        )
    response.raise_for_status()
    return response.json()


def get_field(fields: dict, name: str, raw: bool = False) -> str:
    """Hilfsfunktion: Feldwert aus suggested_fields extrahieren."""
    info = fields.get(name, {})
    if raw:
        return info.get("value_raw", info.get("value", ""))
    return info.get("value", "")


def to_datev_date(iso_date: str) -> str:
    """ISO-Datum (YYYY-MM-DD) → DATEV-Format (DDMM)."""
    parts = iso_date.split("-")
    if len(parts) == 3:
        return f"{parts[2]}{parts[1]}"
    return ""


def to_datev_csv(fields: dict) -> str:
    """Konvertiert IDP-Felder in DATEV-Buchungsstapel CSV."""
    umsatz = get_field(fields, "_total_amount", raw=True)
    datum = get_field(fields, "_invoice_date", raw=True)
    re_nr = get_field(fields, "_invoice_number")
    lieferant = get_field(fields, "_supplier_name")
    ust = get_field(fields, "_vat_rate")

    # BU-Schlüssel aus USt-Satz ableiten
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
        sys.exit("Verwendung: python3 example.py <rechnung.pdf>")

    data = extract_invoice(pdf)
    pages = data.get("result", {}).get("pages_idp", [])
    if not pages:
        sys.exit("Keine IDP-Daten gefunden")

    fields = pages[0].get("suggested_fields", {})

    # Zusammenfassung der extrahierten Felder
    print("--- Extrahierte Rechnungsdaten ---")
    print(f"  Rechnungsnr:  {get_field(fields, '_invoice_number')}")
    print(f"  Datum:        {get_field(fields, '_invoice_date')}")
    print(f"  Lieferant:    {get_field(fields, '_supplier_name')}")
    print(f"  Betrag:       {get_field(fields, '_total_amount')}")
    print(f"  Netto:        {get_field(fields, '_net_amount')}")
    print(f"  USt:          {get_field(fields, '_vat_amount')}")
    print()

    # DATEV-CSV generieren
    datev_csv = to_datev_csv(fields)
    print("--- DATEV Buchungssatz (CSV) ---")
    print(datev_csv)
