#!/usr/bin/env python3
"""
PaperOffice AI — Text-to-Speech (TTS)
Wandelt Text in natürliche Sprache um (100+ Stimmen)

Verwendung:
    export PAPEROFFICE_API_KEY=po_sk_xxx
    python example.py "Hallo Welt" Nadja mp3
"""
import os
import sys
import json
import requests

BASE_URL = "https://api.paperoffice.ai/latest"
API_KEY = os.environ.get("PAPEROFFICE_API_KEY", "")


def text_to_speech(
    text: str,
    voice: str = "Nadja",
    output_format: str = "mp3",
    speed: float = 1.0,
    output: str = "url",
    token: str = API_KEY,
) -> dict:
    """Erzeugt Audio aus Text über die PaperOffice TTS-API."""
    if not token:
        raise ValueError("PAPEROFFICE_API_KEY nicht gesetzt")

    response = requests.post(
        f"{BASE_URL}/job/add/paperoffice_voice___tts",
        headers={"Authorization": f"Bearer {token}"},
        data={
            "text": text,
            "voice": voice,
            "output_format": output_format,
            "output": output,
            "speed": str(speed),
            "priority": "900",
        },
    )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    text = sys.argv[1] if len(sys.argv) > 1 else "Hallo, das ist ein Test der PaperOffice Sprachsynthese."
    voice = sys.argv[2] if len(sys.argv) > 2 else "Nadja"
    fmt = sys.argv[3] if len(sys.argv) > 3 else "mp3"

    data = text_to_speech(text, voice, output_format=fmt)

    result = data.get("result", {})
    print(f"Status:   {data.get('status', 'N/A')}")
    print(f"Stimme:   {result.get('voice', 'N/A')}")
    print(f"Sprache:  {result.get('language', 'N/A')}")
    print(f"Dauer:    {result.get('audio_duration_seconds', 'N/A')}s")
    print(f"Größe:    {result.get('audio_size', 'N/A')} Bytes")
    if result.get("audio_url"):
        print(f"URL:      {result['audio_url']}")
    print()
    print(json.dumps(data, indent=2, ensure_ascii=False))
