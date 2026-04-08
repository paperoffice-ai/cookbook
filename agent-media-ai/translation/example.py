#!/usr/bin/env python3
"""
PaperOffice AI — Text Translation
Translates text between 100+ languages (3 quality tiers)

Usage:
    export PAPEROFFICE_API_KEY=po_sk_xxx
    python example.py "Hello World" de
    python example.py "Hello World" de auto ultra
"""
import os
import sys
import json
import requests

BASE_URL = "https://api.paperoffice.ai/latest"
API_KEY = os.environ.get("PAPEROFFICE_API_KEY", "")


def translate_text(
    text: str,
    target_language: str = "de",
    source_language: str = "auto",
    tier: str = "premium",
    token: str = API_KEY,
) -> dict:
    """Translates text via the PaperOffice Translation API."""
    if not token:
        raise ValueError("PAPEROFFICE_API_KEY not set")

    response = requests.post(
        f"{BASE_URL}/translate/text",
        headers={"Authorization": f"Bearer {token}"},
        data={
            "text": text,
            "target_language": target_language,
            "source_language": source_language,
            "tier": tier,
        },
    )
    response.raise_for_status()
    return response.json()


def list_languages(token: str = API_KEY) -> dict:
    """Returns the list of supported languages."""
    if not token:
        raise ValueError("PAPEROFFICE_API_KEY not set")

    response = requests.get(
        f"{BASE_URL}/translate/languages",
        headers={"Authorization": f"Bearer {token}"},
    )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    text = sys.argv[1] if len(sys.argv) > 1 else "Hello World"
    target = sys.argv[2] if len(sys.argv) > 2 else "de"
    source = sys.argv[3] if len(sys.argv) > 3 else "auto"
    tier = sys.argv[4] if len(sys.argv) > 4 else "premium"

    data = translate_text(text, target, source, tier)

    result = data.get("data", {})
    print(f"Status:       {data.get('status', 'N/A')}")
    print(f"Translation:  {result.get('translation', 'N/A')}")
    print(f"Source lang:  {result.get('source_language', 'N/A')}")
    print(f"Target lang:  {result.get('target_language', 'N/A')}")
    print(f"Tier:         {result.get('tier', 'N/A')}")
    print(f"Characters:   {result.get('characters', 'N/A')}")
    print()
    print(json.dumps(data, indent=2, ensure_ascii=False))
