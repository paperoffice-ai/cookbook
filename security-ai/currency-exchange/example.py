#!/usr/bin/env python3
"""PaperOffice AI — Query exchange rates (VISITOR-capable, no token required)"""
import os
import sys
import requests

API_URL = "https://api.paperoffice.ai/latest/currency_exchange/get_rates"


def get_exchange_rates(from_currency: str = "EUR", to_currency: str = None, amount: float = 1) -> dict:
    """Fetches current exchange rates for 172+ currencies."""
    payload = {"base": from_currency, "amount": amount}
    if to_currency:
        payload["symbols"] = to_currency

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

    print(f"Base:       {data.get('base')}")
    print(f"Amount:     {data.get('amount')}")
    print(f"Currencies: {data.get('currencies_count')}")

    rates = data.get("rates", {})
    top_currencies = ["USD", "GBP", "CHF", "JPY", "CNY"]
    for cur in top_currencies:
        if cur in rates:
            print(f"  {cur}: {rates[cur]}")
