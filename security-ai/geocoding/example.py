#!/usr/bin/env python3
"""PaperOffice AI — Geocoding (address → coordinates and vice versa)"""
import os
import sys
import requests

FORWARD_URL = "https://api.paperoffice.ai/latest/geocoding/forward"
REVERSE_URL = "https://api.paperoffice.ai/latest/geocoding/reverse"
API_KEY = os.environ.get("PAPEROFFICE_API_KEY", "")


def geocode_forward(address: str, lang: str = "en", token: str = API_KEY) -> dict:
    """Converts an address into coordinates."""
    if not token:
        raise ValueError("PAPEROFFICE_API_KEY not set")

    response = requests.post(
        FORWARD_URL,
        headers={"Authorization": f"Bearer {token}"},
        data={"address": address, "lang": lang},
    )
    response.raise_for_status()
    return response.json()


def geocode_reverse(lat: float, lng: float, lang: str = "en", token: str = API_KEY) -> dict:
    """Converts coordinates into an address."""
    if not token:
        raise ValueError("PAPEROFFICE_API_KEY not set")

    response = requests.post(
        REVERSE_URL,
        headers={"Authorization": f"Bearer {token}"},
        data={"lat": lat, "lng": lng, "lang": lang},
    )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    address = sys.argv[1] if len(sys.argv) > 1 else "Berlin, Germany"

    print(f"=== Forward: {address} ===")
    fwd = geocode_forward(address)
    if fwd.get("found"):
        print(f"Lat:     {fwd.get('lat')}")
        print(f"Lng:     {fwd.get('lng')}")
        print(f"Address: {fwd.get('display_name')}")

    print(f"\n=== Reverse: 52.5174, 13.3951 ===")
    rev = geocode_reverse(52.5174, 13.3951)
    if rev.get("found"):
        print(f"Address: {rev.get('display_name')}")
