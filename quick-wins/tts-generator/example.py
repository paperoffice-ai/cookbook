#!/usr/bin/env python3
"""
PaperOffice AI — Text-to-Speech Generator
Bearer Token ERFORDERLICH

Verwendung:
    export PAPEROFFICE_API_KEY=po_sk_xxx
    python example.py "Hallo Welt" Nadja
"""
import os
import sys
import requests

API_URL = "https://api.paperoffice.ai/latest/job"
API_KEY = os.environ.get("PAPEROFFICE_API_KEY", "")


def text_to_speech(
    text: str,
    voice: str = "Nadja",
    output_format: str = "mp3",
    speed: float = 1.0,
    token: str = API_KEY,
) -> dict:
    """Generiert Audio aus Text mit neuronalen Stimmen."""
    if not token:
        raise ValueError("PAPEROFFICE_API_KEY nicht gesetzt")

    response = requests.post(
        API_URL,
        headers={"Authorization": f"Bearer {token}"},
        data={
            "text": text,
            "voice": voice,
            "output_format": output_format,
            "output": "url",
            "speed": str(speed),
            "priority": 999,
        },
    )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    text = sys.argv[1] if len(sys.argv) > 1 else "Hallo, das ist ein Test der Sprachausgabe."
    voice = sys.argv[2] if len(sys.argv) > 2 else "Nadja"
    result = text_to_speech(text, voice)
    print(f"Audio: {result.get('job_result', {}).get('audio_url', 'N/A')}")
