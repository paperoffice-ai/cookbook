#!/usr/bin/env python3
"""
PaperOffice AI — Speech-to-Text (STT)
Transkribiert Audio-Dateien in Text

Verwendung:
    export PAPEROFFICE_API_KEY=po_sk_xxx
    python example.py audio.mp3
    python example.py audio.mp3 de
"""
import os
import sys
import json
import requests

BASE_URL = "https://api.paperoffice.ai/latest"
API_KEY = os.environ.get("PAPEROFFICE_API_KEY", "")


def speech_to_text(
    audio_path: str,
    locale: str | None = None,
    token: str = API_KEY,
) -> dict:
    """Transkribiert eine Audio-Datei über die PaperOffice STT-API."""
    if not token:
        raise ValueError("PAPEROFFICE_API_KEY nicht gesetzt")

    if not os.path.isfile(audio_path):
        raise FileNotFoundError(f"Datei nicht gefunden: {audio_path}")

    # Datei-Key ist "file_1" — NICHT "file"!
    with open(audio_path, "rb") as f:
        files = {"file_1": (os.path.basename(audio_path), f)}
        data = {"priority": "900"}
        if locale:
            data["locale"] = locale

        response = requests.post(
            f"{BASE_URL}/job/add/paperoffice_voice___stt",
            headers={"Authorization": f"Bearer {token}"},
            files=files,
            data=data,
        )

    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Verwendung: python example.py <audio_datei> [locale]")
        sys.exit(1)

    audio_path = sys.argv[1]
    locale = sys.argv[2] if len(sys.argv) > 2 else None

    data = speech_to_text(audio_path, locale)

    result = data.get("result", {})
    print(f"Status:   {data.get('status', 'N/A')}")
    print(f"Text:     {result.get('text', 'N/A')}")
    print(f"Sprache:  {result.get('language', 'N/A')}")
    print(f"Dauer:    {result.get('audio_duration_seconds', 'N/A')}s")
    print(f"Qualität: {result.get('quality', 'N/A')}")
    print()
    print(json.dumps(data, indent=2, ensure_ascii=False))
