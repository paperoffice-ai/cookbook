#!/usr/bin/env python3
"""PaperOffice AI — Detect fake email"""
import os
import sys
import requests

API_URL = "https://api.paperoffice.ai/latest/fakeemail/check"
BULK_URL = "https://api.paperoffice.ai/latest/fakeemail/check_bulk"
API_KEY = os.environ.get("PAPEROFFICE_API_KEY", "")


def check_email(email: str, token: str = API_KEY) -> dict:
    """Checks a single email address for fake/disposable characteristics."""
    if not token:
        raise ValueError("PAPEROFFICE_API_KEY not set")

    response = requests.post(
        API_URL,
        headers={"Authorization": f"Bearer {token}"},
        data={"email": email},
    )
    response.raise_for_status()
    return response.json()


def check_emails_bulk(emails: list, token: str = API_KEY) -> dict:
    """Checks up to 100 email addresses at once."""
    if not token:
        raise ValueError("PAPEROFFICE_API_KEY not set")

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
    print(f"Email:       {result.get('email')}")
    print(f"Is fake:     {result.get('is_fake')}")
    print(f"Risk score:  {result.get('risk_score')}")
    print(f"Risk level:  {result.get('risk_level')}")
    print(f"Recommendation:{result.get('recommendation')}")
    print(f"Method:      {result.get('detection_method')}")
