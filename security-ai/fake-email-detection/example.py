#!/usr/bin/env python3
"""PaperOffice AI — Fake-E-Mail erkennen"""
import os
import sys
import requests

API_URL = "https://api.paperoffice.ai/latest/fakeemail/check"
BULK_URL = "https://api.paperoffice.ai/latest/fakeemail/check_bulk"
API_KEY = os.environ.get("PAPEROFFICE_API_KEY", "")


def check_email(email: str, token: str = API_KEY) -> dict:
    """Prüft eine einzelne E-Mail-Adresse auf Fake/Wegwerf-Charakter."""
    if not token:
        raise ValueError("PAPEROFFICE_API_KEY nicht gesetzt")

    response = requests.post(
        API_URL,
        headers={"Authorization": f"Bearer {token}"},
        data={"email": email},
    )
    response.raise_for_status()
    return response.json()


def check_emails_bulk(emails: list, token: str = API_KEY) -> dict:
    """Prüft bis zu 100 E-Mail-Adressen gleichzeitig."""
    if not token:
        raise ValueError("PAPEROFFICE_API_KEY nicht gesetzt")

    response = requests.post(
        BULK_URL,
        headers={"Authorization": f"Bearer {token}"},
        data={"emails": emails},
    )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    email = sys.argv[1] if len(sys.argv) > 1 else "test@mailinator.com"
    data = check_email(email)

    result = data.get("result", {})
    print(f"E-Mail:      {result.get('email')}")
    print(f"Ist Fake:    {result.get('is_fake')}")
    print(f"Risiko-Score:{result.get('risk_score')}")
    print(f"Risiko-Level:{result.get('risk_level')}")
    print(f"Empfehlung:  {result.get('recommendation')}")
    print(f"Methode:     {result.get('detection_method')}")
