#!/usr/bin/env python3
"""
PaperOffice AI — Webhook-basierte Verarbeitung
Registriert Webhooks und verarbeitet Events in Echtzeit.

Verwendung:
    export PAPEROFFICE_API_KEY=po_sk_xxx
    python pipeline.py
"""
import os
import hmac
import hashlib
from flask import Flask, request

API_URL = "https://api.paperoffice.ai/latest"
API_KEY = os.environ.get("PAPEROFFICE_API_KEY", "")
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", "your_webhook_secret")

app = Flask(__name__)


def setup_webhook(callback_url: str, token: str = API_KEY):
    """Registriert einen Webhook für Job-Events."""
    import requests

    if not token:
        raise ValueError("PAPEROFFICE_API_KEY nicht gesetzt")

    response = requests.post(
        f"{API_URL}/webhooks",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "url": callback_url,
            "events": ["job.completed", "job.failed"],
            "secret": WEBHOOK_SECRET,
        },
    )
    response.raise_for_status()
    print(f"✓ Webhook registriert: {callback_url}")
    return response.json()


@app.route("/webhook", methods=["POST"])
def handle_webhook():
    """Empfängt und verifiziert Webhook-Events."""
    signature = request.headers.get("X-PaperOffice-Signature", "")
    expected = hmac.new(
        WEBHOOK_SECRET.encode(), request.data, hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(signature, expected):
        return "Invalid signature", 401

    event = request.json
    event_type = event.get("event", "")

    if event_type == "job.completed":
        print(f"✓ Job fertig: {event.get('job_id')}")
        process_result(event.get("result", {}))
    elif event_type == "job.failed":
        print(f"✗ Job fehlgeschlagen: {event.get('job_id')}")

    return "OK", 200


def process_result(result: dict):
    """Verarbeitet das Ergebnis eines abgeschlossenen Jobs."""
    fulltext = result.get("fulltext", "")
    idp = result.get("pages_idp", [])
    print(f"  Volltext: {len(fulltext)} Zeichen")
    print(f"  IDP-Seiten: {len(idp)}")
    print(f"  Ergebnis-Keys: {list(result.keys())}")


if __name__ == "__main__":
    print("→ Starte Webhook-Server auf Port 5000...")
    print("  Registriere Webhook mit: setup_webhook('https://your-server.com/webhook')")
    app.run(port=5000, debug=True)
