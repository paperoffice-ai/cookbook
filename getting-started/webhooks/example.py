#!/usr/bin/env python3
"""PaperOffice AI — Webhooks (Subscribe + Receiver)"""
import os
import sys
import hmac
import hashlib
import requests

api_base = "https://api.paperoffice.ai/latest"
api_key = os.environ.get("PAPEROFFICE_API_KEY")
if not api_key:
    sys.exit("Fehler: PAPEROFFICE_API_KEY nicht gesetzt")

headers = {"Authorization": f"Bearer {api_key}"}
webhook_secret = "mein_webhook_secret_123"


def subscribe_webhook(url, events):
    """Webhook bei PaperOffice registrieren."""
    response = requests.post(
        f"{api_base}/webhooks/subscribe",
        headers={**headers, "Content-Type": "application/json"},
        json={
            "name": "mein_erster_webhook",
            "url": url,
            "events": events,
            "secret": webhook_secret,
        },
    )
    return response.json()


def list_webhooks():
    """Alle registrierten Webhooks abrufen."""
    response = requests.get(f"{api_base}/webhooks/list", headers=headers)
    return response.json()


def verify_signature(payload_body, signature):
    """Webhook-Signatur mit HMAC-SHA256 verifizieren."""
    expected = hmac.new(
        webhook_secret.encode(),
        payload_body,
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(expected, signature)


# --- Webhook registrieren und auflisten ---
if __name__ == "__main__":
    webhook_url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com/webhook"

    print(">>> Webhook registrieren...")
    result = subscribe_webhook(webhook_url, ["job.completed", "job.failed"])
    print(result)

    print("\n>>> Webhooks auflisten...")
    webhooks = list_webhooks()
    print(f"Gesamt: {webhooks.get('total', 0)}")
    for sub in webhooks.get("subscriptions", []):
        print(f"  - {sub.get('name')}: {sub.get('url')}")

    # --- Flask-basierter Receiver (optional starten mit: python example.py serve) ---
    if len(sys.argv) > 1 and sys.argv[1] == "serve":
        try:
            from flask import Flask, request, jsonify
        except ImportError:
            sys.exit("Flask nicht installiert: pip install flask")

        app = Flask(__name__)

        @app.route("/webhook", methods=["POST"])
        def receive_webhook():
            signature = request.headers.get("X-PaperOffice-Signature", "")
            if not verify_signature(request.get_data(), signature):
                return jsonify({"error": "Ungültige Signatur"}), 401

            event = request.json
            print(f"Webhook empfangen: {event.get('event')}")
            print(f"  Job-ID: {event.get('job_id')}")
            print(f"  Status: {event.get('status')}")
            return jsonify({"received": True}), 200

        print("\n>>> Webhook-Receiver läuft auf http://localhost:5000/webhook")
        app.run(port=5000)
