#!/usr/bin/env python3
"""
PaperOffice AI — Speech-to-Text (STT)
Transcribes audio files to text

Usage:
    export PAPEROFFICE_API_KEY=po_ut_xxx
    python example.py audio.mp3
    python example.py audio.mp3 de
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


def speech_to_text(
    audio_path: str,
    locale: str | None = None,
    token: str = API_KEY,
) -> dict:
    """Transcribes an audio file via the PaperOffice STT API."""
    if not token:
        raise ValueError("PAPEROFFICE_API_KEY not set")

    if not os.path.isfile(audio_path):
        raise FileNotFoundError(f"File not found: {audio_path}")

    # File key is "file_1" — NOT "file"!
    with open(audio_path, "rb") as f:
        files = {"file_1": (os.path.basename(audio_path), f)}
        data = {"processing_lane": "instant"}
        if locale:
            data["locale"] = locale

        response = requests.post(
            f"{BASE_URL}/job/add/paperoffice_voice___stt",
            headers={"Authorization": f"Bearer {token}"},
            files=files,
            data=data,
        )

    response.raise_for_status()
    return wait_for_result(response.json(), token)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python example.py <audio_file> [locale]")
        sys.exit(1)

    audio_path = sys.argv[1]
    locale = sys.argv[2] if len(sys.argv) > 2 else None

    data = speech_to_text(audio_path, locale)

    result = data.get("result", {})
    print(f"Status:   {data.get('status', 'N/A')}")
    print(f"Text:     {result.get('text', 'N/A')}")
    print(f"Language: {result.get('language', 'N/A')}")
    print(f"Duration: {result.get('audio_duration_seconds', 'N/A')}s")
    print(f"Quality:  {result.get('quality', 'N/A')}")
    print()
    print(json.dumps(data, indent=2, ensure_ascii=False))
