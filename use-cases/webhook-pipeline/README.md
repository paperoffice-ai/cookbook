# Webhook Pipeline

Webhook-basierte Echtzeit-Verarbeitung: Jobs absenden, Events empfangen, Ergebnisse verarbeiten.

## Workflow

```
1. Webhook registrieren (POST /webhooks)
2. Job absenden (async, priority < 900)
3. Webhook empfängt job.completed Event
4. Ergebnis verarbeiten
```

## Voraussetzungen

```bash
export PAPEROFFICE_API_KEY=po_sk_xxx
export WEBHOOK_SECRET=your_secret
pip install requests flask
```

## Verwendung

```bash
python pipeline.py
```

Startet einen Flask-Server auf Port 5000 der Webhook-Events empfängt.

## Sicherheit

- Jeder Webhook wird mit HMAC-SHA256 signiert
- `X-PaperOffice-Signature` Header enthält die Signatur
- Server verifiziert die Signatur vor Verarbeitung
