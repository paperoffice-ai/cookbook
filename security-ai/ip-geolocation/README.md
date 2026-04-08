# IP-Geolocation — Standort & Gerätedaten

Ermittelt den physischen Standort, Geräteinformationen und Wechselkurse für eine IP-Adresse. Ohne IP-Parameter wird die eigene IP des Aufrufers verwendet.

## Endpoint

```
POST https://api.paperoffice.ai/latest/ip2location/full
```

**Authentifizierung:** VISITOR-fähig (IP-Ratelimit), empfohlen mit Bearer Token.

## Parameter

| Parameter | Typ | Pflicht | Beschreibung |
|---|---|---|---|
| `ip` | string | ❌ | IP-Adresse (Standard: eigene IP) |
| `locale` | string | ❌ | Sprache der Antwort (Standard: `de`) |

## Ausführen

```bash
export PAPEROFFICE_API_KEY=po_sk_xxx

# Bash — eigene IP
bash example.sh

# Bash — bestimmte IP
bash example.sh "8.8.8.8"

# Python
pip install requests
python3 example.py "8.8.8.8"

# Node.js (v18+)
node example.js "8.8.8.8"
```

## Erwartete Antwort (gekürzt)

```json
{
    "country": "DE",
    "country_name": "Deutschland",
    "city": "Frankfurt am Main",
    "latitude": 50.1109,
    "longitude": 8.6821,
    "timezone": "Europe/Berlin",
    "device": {
        "os": "Linux",
        "browser": "curl"
    },
    "exchange_rates": {
        "EUR": 1.0,
        "USD": 1.0862
    }
}
```

## Anwendungsfälle

- **Geo-Blocking:** Zugriff auf Inhalte nach Land einschränken
- **Betrugserkennung:** IP-Standort mit Rechnungsadresse vergleichen
- **Lokalisierung:** Sprache, Währung und Steuersätze automatisch anpassen
