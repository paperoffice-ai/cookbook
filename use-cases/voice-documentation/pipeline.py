#!/usr/bin/env python3
"""
PaperOffice AI — Voice Documentation
Dokument → OCR → Text → TTS → Audio-Dateien

Verwendung:
    export PAPEROFFICE_API_KEY=po_sk_xxx
    python pipeline.py handbuch.pdf
    python pipeline.py handbuch.pdf Thomas  # andere Stimme
"""
import os
import sys
import requests

API_URL = "https://api.paperoffice.ai/latest/job"
API_KEY = os.environ.get("PAPEROFFICE_API_KEY", "")

MAX_TTS_CHARS = 5000


def document_to_audio(
    pdf_path: str, voice: str = "Nadja", token: str = API_KEY
) -> list[str]:
    """Konvertiert ein Dokument in Audio-Dateien (OCR → TTS)."""
    if not token:
        raise ValueError("PAPEROFFICE_API_KEY nicht gesetzt")

    headers = {"Authorization": f"Bearer {token}"}

    # Schritt 1: OCR — Text extrahieren
    print("→ Schritt 1: OCR...")
    ocr_response = requests.post(
        API_URL,
        headers=headers,
        files={"file_1": open(pdf_path, "rb")},
        data={"ocr_mode": "complete", "priority": 900},
    )
    ocr_response.raise_for_status()

    text = ocr_response.json().get("job_result", {}).get("text", "")
    if not text:
        print("  ✗ Kein Text gefunden")
        return []

    print(f"  ✓ {len(text)} Zeichen extrahiert")

    # Schritt 2: Text in Abschnitte teilen
    chunks = [text[i : i + MAX_TTS_CHARS] for i in range(0, len(text), MAX_TTS_CHARS)]
    print(f"→ Schritt 2: {len(chunks)} Audio-Abschnitte generieren...")

    # Schritt 3: TTS für jeden Abschnitt
    audio_urls = []
    for i, chunk in enumerate(chunks):
        print(f"  TTS {i + 1}/{len(chunks)}...")
        tts_response = requests.post(
            API_URL,
            headers=headers,
            data={
                "text": chunk,
                "voice": voice,
                "output_format": "mp3",
                "output": "url",
                "priority": 999,
            },
        )
        tts_response.raise_for_status()
        url = tts_response.json().get("job_result", {}).get("audio_url", "")
        if url:
            audio_urls.append(url)

    print(f"✓ {len(audio_urls)} Audio-Dateien generiert")
    return audio_urls


if __name__ == "__main__":
    pdf = sys.argv[1] if len(sys.argv) > 1 else "handbuch.pdf"
    voice = sys.argv[2] if len(sys.argv) > 2 else "Nadja"

    urls = document_to_audio(pdf, voice)
    for i, url in enumerate(urls):
        print(f"  Audio {i + 1}: {url}")
