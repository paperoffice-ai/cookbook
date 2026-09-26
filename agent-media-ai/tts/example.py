#!/usr/bin/env python3
"""
PaperOffice AI — Text-to-Speech (TTS)
Converts text to natural speech (100+ voices)

Usage:
    export PAPEROFFICE_API_KEY=po_ut_xxx
    python example.py "Hallo Welt" Nadja mp3
"""
import os
import sys
import json
import requests

def wait_for_result(data: dict, token: str, api_base: str = "https://api.paperoffice.ai/latest", timeout_s: int = 180) -> dict:
    """HTTP 202 means the job is still running: follow job/get until it is completed."""
    if data.get("result") or not data.get("job_id"):
        return data
    import time
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        time.sleep(2)
        poll = requests.get(f"{api_base}/job/get/{data['job_id']}", headers={"Authorization": f"Bearer {token}"}).json()
        if poll.get("job_status") == "completed" or poll.get("result") or poll.get("job_result"):
            # job/get returns the payload as job_result — expose it under result like the inline response
            if "result" not in poll and "job_result" in poll:
                poll["result"] = poll["job_result"]
            return poll
        if poll.get("job_status") in ("failed", "error") or poll.get("status") == "error":
            raise RuntimeError(f"job failed: {poll.get('message')}")
    raise TimeoutError(f"job {data['job_id']} not finished after {timeout_s}s")


BASE_URL = "https://api.paperoffice.ai/latest"
API_KEY = os.environ.get("PAPEROFFICE_API_KEY", "")


def text_to_speech(
    text: str,
    voice: str = "Nadja",
    language: str = "de",
    output_format: str = "mp3",
    speed: float = 1.0,
    output: str = "url",
    token: str = API_KEY,
) -> dict:
    """Generates audio from text via the PaperOffice TTS API."""
    if not token:
        raise ValueError("PAPEROFFICE_API_KEY not set")

    response = requests.post(
        f"{BASE_URL}/job/add/paperoffice_voice___tts",
        headers={"Authorization": f"Bearer {token}"},
        data={
            "text": text,
            "voice": voice,
            "language": language,
            "output_format": output_format,
            "output": output,
            "speed": str(speed),
            "processing_lane": "instant",
        },
    )
    response.raise_for_status()
    return wait_for_result(response.json(), token)


if __name__ == "__main__":
    text = sys.argv[1] if len(sys.argv) > 1 else "Hallo, das ist ein Test der PaperOffice Sprachsynthese."
    voice = sys.argv[2] if len(sys.argv) > 2 else "Nadja"
    language = sys.argv[3] if len(sys.argv) > 3 else "de"
    fmt = sys.argv[4] if len(sys.argv) > 4 else "mp3"

    data = text_to_speech(text, voice, language=language, output_format=fmt)

    result = data.get("result", {})
    print(f"Status:   {data.get('status', 'N/A')}")
    print(f"Voice:    {result.get('voice', 'N/A')}")
    print(f"Language: {result.get('language', 'N/A')}")
    print(f"Duration: {result.get('audio_duration_seconds', 'N/A')}s")
    print(f"Size:     {result.get('audio_size', 'N/A')} Bytes")
    if result.get("audio_url"):
        print(f"URL:      {result['audio_url']}")
    print()
    print(json.dumps(data, indent=2, ensure_ascii=False))
