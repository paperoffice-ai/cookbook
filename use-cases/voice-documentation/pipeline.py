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
import json
import requests

OCR_URL = "https://api.paperoffice.ai/latest/job/add/workflow"
TTS_URL = "https://api.paperoffice.ai/latest/voice/tts"
API_KEY = os.environ.get("PAPEROFFICE_API_KEY", "")

MAX_TTS_CHARS = 5000


def document_to_audio(
    pdf_path: str, voice: str = "Nadja", token: str = API_KEY
) -> list[dict]:
    """Konvertiert ein Dokument in Audio-Dateien (OCR → TTS)."""
    if not token:
        raise ValueError("PAPEROFFICE_API_KEY nicht gesetzt")

    headers = {"Authorization": f"Bearer {token}"}

    # Schritt 1: OCR — Text extrahieren
    print("→ Schritt 1: OCR...")
    ocr_response = requests.post(
        OCR_URL,
        headers=headers,
        files={"file_1": open(pdf_path, "rb")},
        data={"ocr_mode": "complete", "priority": 900},
    )
    ocr_response.raise_for_status()

    result = ocr_response.json().get("result", {})
    text = result.get("fulltext", "")
    if not text:
        print("  ✗ Kein Text gefunden")
        return []

    print(f"  ✓ {len(text)} Zeichen extrahiert")

    # Schritt 2: Text in Abschnitte teilen
    chunks = [text[i : i + MAX_TTS_CHARS] for i in range(0, len(text), MAX_TTS_CHARS)]
    print(f"→ Schritt 2: {len(chunks)} Audio-Abschnitte generieren...")

    # Schritt 3: TTS für jeden Abschnitt
    tts_results = []
    for i, chunk in enumerate(chunks):
        print(f"  TTS {i + 1}/{len(chunks)}...")
        tts_response = requests.post(
            TTS_URL,
            headers=headers,
            data={
                "text": chunk,
                "voice": voice,
                "output_format": "mp3",
                "output": "url",
                "priority": 900,
            },
        )
        tts_response.raise_for_status()
        tts_data = tts_response.json()
        tts_results.append({
            "chunk": i + 1,
            "status": tts_data.get("status", "unknown"),
            "processing_time": tts_data.get("processing_time", "N/A"),
        })

    print(f"✓ {len(tts_results)} Audio-Abschnitte verarbeitet")
    return tts_results


if __name__ == "__main__":
    pdf = sys.argv[1] if len(sys.argv) > 1 else "handbuch.pdf"
    voice = sys.argv[2] if len(sys.argv) > 2 else "Nadja"

    results = document_to_audio(pdf, voice)
    for r in results:
        print(f"  Chunk {r['chunk']}: {r['status']} ({r['processing_time']})")
