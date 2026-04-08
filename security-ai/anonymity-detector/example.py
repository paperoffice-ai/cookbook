#!/usr/bin/env python3
"""PaperOffice AI — VPN/Proxy/Tor-Erkennung"""
import os
import sys
import requests

API_URL = "https://api.paperoffice.ai/latest/ip2location/vpn"
API_KEY = os.environ.get("PAPEROFFICE_API_KEY", "")


def detect_anonymity(ip: str = None, token: str = API_KEY) -> dict:
    """Erkennt VPN, Proxy, Tor, Datacenter und Relay für eine IP-Adresse."""
    if not token:
        raise ValueError("PAPEROFFICE_API_KEY nicht gesetzt")

    payload = {}
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
    data = detect_anonymity(ip=ip_addr)

    print(f"VPN:        {data.get('is_vpn')}")
    print(f"Proxy:      {data.get('is_proxy')}")
    print(f"Tor:        {data.get('is_tor')}")
    print(f"Datacenter: {data.get('is_datacenter')}")
    print(f"Relay:      {data.get('is_relay')}")
    print(f"Score:      {data.get('score')}%")
