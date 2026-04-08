# Webhooks — Event-Benachrichtigungen

Statt ständig den Job-Status zu pollen, kannst du Webhooks registrieren und wirst aktiv benachrichtigt wenn ein Ereignis eintritt.

## Endpoints

| Aktion     | Methode | Endpoint              |
|-----------|---------|-----------------------|
| Subscribe | POST    | `/webhooks/subscribe` |
| Auflisten | GET     | `/webhooks/list`      |
| Testen    | POST    | `/webhooks/test`      |

**Authentifizierung:** Bearer Token für alle Endpoints

## Subscribe-Parameter

```json
{
  "name": "mein_erster_webhook",
  "url": "https://mein-server.de/webhook",
  "events": ["job.completed", "job.failed"],
  "secret": "mein_geheimer_schlüssel"
}
```

| Parameter | Pflicht | Beschreibung                              |
|----------|---------|-------------------------------------------|
| `name`   | Ja      | Eindeutiger Name für den Webhook          |
| `url`    | Ja      | HTTPS-URL die aufgerufen wird             |
| `events` | Ja      | Array von Event-Typen                     |
| `secret` | Nein    | Shared Secret für Signatur-Verifizierung  |
| `filters`| Nein    | Zusätzliche Filter (z.B. nach Tool-ID)    |

## Verfügbare Events

| Event            | Beschreibung                    |
|-----------------|---------------------------------|
| `job.completed` | Job erfolgreich abgeschlossen   |
| `job.failed`    | Job fehlgeschlagen              |
| `job.queued`    | Job in die Queue eingereiht     |

## Signatur-Verifizierung

Jeder Webhook-Call enthält einen `X-PaperOffice-Signature` Header. Damit stellst du sicher, dass der Call wirklich von PaperOffice kommt:

```python
import hmac, hashlib

expected = hmac.new(
    secret.encode(),
    request_body,
    hashlib.sha256
).hexdigest()

is_valid = hmac.compare_digest(expected, received_signature)
```

## Ausführen

```bash
export PAPEROFFICE_API_KEY="dein_api_key"

# Webhook registrieren (Bash)
chmod +x example.sh && ./example.sh https://mein-server.de/webhook

# Python — Registrieren + Receiver starten
pip install requests flask
python3 example.py https://mein-server.de/webhook   # Nur registrieren
python3 example.py serve                              # Receiver starten

# Node.js (v18+)
node example.js https://mein-server.de/webhook   # Nur registrieren
node example.js serve                             # Receiver starten
```

## Webhook vs. Polling

| Aspekt       | Polling                     | Webhooks                       |
|-------------|-----------------------------|--------------------------------|
| Latenz      | Abhängig vom Intervall      | Quasi-Echtzeit                 |
| Traffic     | Viele unnötige Requests     | Nur bei tatsächlichen Events   |
| Komplexität | Einfacher zu implementieren | Braucht öffentlichen Endpoint  |
| Zuverlässig | Immer (Pull-basiert)        | Retry-Logik nötig              |
