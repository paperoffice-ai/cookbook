#!/usr/bin/env python3
"""PaperOffice AI — Verify device fingerprint"""
import os
import sys
import requests

API_URL = "https://api.paperoffice.ai/latest/fingerprint/verify"
API_KEY = os.environ.get("PAPEROFFICE_API_KEY", "")


def verify_fingerprint(visitor_id: str, token: str = API_KEY) -> dict:
    """Checks whether a device is known and trusted."""
    if not token:
        raise ValueError("PAPEROFFICE_API_KEY not set")

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

    print(f"Visitor ID:  {data.get('visitorId')}")
    print(f"Verified:    {data.get('verified')}")
    print(f"Reason:      {data.get('reason')}")
    print(f"Status:      {data.get('status')}")
