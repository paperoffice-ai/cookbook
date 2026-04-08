#!/usr/bin/env python3
"""PaperOffice AI — Query IP geolocation"""
import os
import sys
import json
import requests

API_URL = "https://api.paperoffice.ai/latest/ip2location/full"
API_KEY = os.environ.get("PAPEROFFICE_API_KEY", "")


def get_geolocation(ip: str = None, locale: str = "de", token: str = API_KEY) -> dict:
    """Retrieves location, device data, and exchange rates for an IP address."""
    if not token:
        raise ValueError("PAPEROFFICE_API_KEY not set")

    payload = {"locale": locale}
    if ip:
        payload["ip"] = ip

    response = requests.post(
        API_URL,
        headers={"Authorization": f"Bearer {token}"},
        data=payload,
    )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    ip_addr = sys.argv[1] if len(sys.argv) > 1 else None
    data = get_geolocation(ip=ip_addr)

    print(json.dumps(data, indent=2, ensure_ascii=False))
