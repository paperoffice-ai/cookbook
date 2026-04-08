# Device Fingerprint — Geräte-Verifizierung

Prüft ob ein Gerät (Browser/App) bekannt und vertrauenswürdig ist. Ideal für Betrugs-Erkennung, Account-Sicherheit und Multi-Device-Tracking.

## Endpoint

```
POST https://api.paperoffice.ai/latest/fingerprint/verify
```

**Authentifizierung:** Bearer Token erforderlich.

## Parameter

| Parameter | Typ | Pflicht | Beschreibung |
|---|---|---|---|
| `visitorId` | string | ✅ | Eindeutige Geräte-ID (z.B. aus FingerprintJS) |

## Ausführen

```bash
export PAPEROFFICE_API_KEY=po_sk_xxx

# Bash
bash example.sh "visitor_abc123"

# Python
pip install requests
python3 example.py "visitor_abc123"

# Node.js (v18+)
node example.js "visitor_abc123"
```

## Erwartete Antwort

```json
{
    "verified": false,
    "visitorId": "visitor_abc123",
    "reason": "unknown_device",
    "status": "success"
}
```

## Anwendungsfälle

- **Login-Schutz:** Unbekannte Geräte bei sensiblen Aktionen blockieren oder 2FA erzwingen
- **Betrugs-Erkennung:** Auffällige Geräte-Wechsel erkennen
- **Account-Sharing:** Erkennen, wenn ein Account von zu vielen Geräten genutzt wird
