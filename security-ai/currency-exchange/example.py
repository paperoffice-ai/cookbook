#!/usr/bin/env python3
"""PaperOffice AI — Wechselkurse abfragen (VISITOR-fähig, kein Token nötig)"""
import os
import sys
import requests

API_URL = "https://api.paperoffice.ai/latest/currency_exchange/get_rates"


def get_exchange_rates(from_currency: str = "EUR", to_currency: str = None, amount: float = 1) -> dict:
    """Ruft aktuelle Wechselkurse für 172+ Währungen ab."""
    payload = {"from": from_currency, "amount": amount}
    if to_currency:
        payload["to"] = to_currency

    headers = {}
    api_key = os.environ.get("PAPEROFFICE_API_KEY", "")
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    response = requests.post(
        API_URL,
        headers=headers,
        data=payload,
    )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    from_cur = sys.argv[1] if len(sys.argv) > 1 else "EUR"
    to_cur = sys.argv[2] if len(sys.argv) > 2 else None
    amount = float(sys.argv[3]) if len(sys.argv) > 3 else 100

    data = get_exchange_rates(from_cur, to_cur, amount)

    print(f"Basis:    {data.get('base')}")
    print(f"Betrag:   {data.get('amount')}")
    print(f"Währungen:{data.get('currencies_count')}")

    rates = data.get("rates", {})
    top_currencies = ["USD", "GBP", "CHF", "JPY", "CNY"]
    for cur in top_currencies:
        if cur in rates:
            print(f"  {cur}: {rates[cur]}")
