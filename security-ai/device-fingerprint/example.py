#!/usr/bin/env python3
"""PaperOffice AI — Device Fingerprint verifizieren"""
import os
import sys
import requests

API_URL = "https://api.paperoffice.ai/latest/fingerprint/verify"
API_KEY = os.environ.get("PAPEROFFICE_API_KEY", "")


def verify_fingerprint(visitor_id: str, token: str = API_KEY) -> dict:
    """Prüft ob ein Gerät bekannt und vertrauenswürdig ist."""
    if not token:
        raise ValueError("PAPEROFFICE_API_KEY nicht gesetzt")

    response = requests.post(
        API_URL,
        headers={"Authorization": f"Bearer {token}"},
        data={"visitorId": visitor_id},
    )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    vid = sys.argv[1] if len(sys.argv) > 1 else "test_visitor_abc123"
    data = verify_fingerprint(vid)

    print(f"Visitor-ID:  {data.get('visitorId')}")
    print(f"Verifiziert: {data.get('verified')}")
    print(f"Grund:       {data.get('reason')}")
    print(f"Status:      {data.get('status')}")
