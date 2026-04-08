#!/usr/bin/env python3
"""PaperOffice AI — Validate VAT ID"""
import os
import sys
import json
import requests

API_URL = "https://api.paperoffice.ai/latest/vat/validate"
RATES_URL = "https://api.paperoffice.ai/latest/vat/rates"
API_KEY = os.environ.get("PAPEROFFICE_API_KEY", "")


def validate_vat(vat_id: str, token: str = API_KEY) -> dict:
    """Validates a European VAT ID (format + VIES)."""
    if not token:
        raise ValueError("PAPEROFFICE_API_KEY not set")

    response = requests.post(
        API_URL,
        headers={"Authorization": f"Bearer {token}"},
        data={"vat_id": vat_id},
    )
    response.raise_for_status()
    return response.json()


def get_vat_rates() -> dict:
    """Fetches current EU tax rates (free, no token required)."""
    response = requests.get(RATES_URL)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    vat = sys.argv[1] if len(sys.argv) > 1 else "DE123456789"

    print(f"=== VAT ID Validation: {vat} ===")
    result = validate_vat(vat)
    print(f"Status:       {result.get('status')}")
    print(f"Format valid: {result.get('format_valid')}")
    if result.get("error"):
        print(f"Error:        {result.get('error')}")
        print(f"Message:      {result.get('message')}")
        print(f"Layer:        {result.get('layer')}")

    print(f"\n=== EU Tax Rates (excerpt) ===")
    rates = get_vat_rates()
    print(json.dumps(rates, indent=2, ensure_ascii=False)[:500])
