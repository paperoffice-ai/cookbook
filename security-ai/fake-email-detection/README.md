# Fake-E-Mail Erkennung

Erkennt Wegwerf-E-Mail-Adressen (Mailinator, Guerrilla Mail etc.), temporäre Domains und verdächtige Muster. Unterstützt Einzel- und Massenprüfung (bis 100 E-Mails).

## Endpoints

```
POST https://api.paperoffice.ai/latest/fakeemail/check
POST https://api.paperoffice.ai/latest/fakeemail/check_bulk
```

**Authentifizierung:** Bearer Token erforderlich.

## Parameter

| Parameter | Typ | Pflicht | Beschreibung |
|---|---|---|---|
| `email` | string | ✅ | Zu prüfende E-Mail-Adresse (Einzel) |
| `emails` | array | ✅ | Bis zu 100 E-Mail-Adressen (Bulk) |

## Ausführen

```bash
export PAPEROFFICE_API_KEY=po_sk_xxx

# Bash
bash example.sh "test@mailinator.com"

# Python
pip install requests
python3 example.py "test@mailinator.com"

# Node.js (v18+)
node example.js "test@mailinator.com"
```

## Erwartete Antwort

```json
{
    "result": {
        "email": "test@mailinator.com",
        "is_fake": true,
        "risk_score": 70,
        "risk_level": "HIGH",
        "detection_method": "HIGH_RISK_SCORE",
        "recommendation": "REJECT",
        "checks": {}
    }
}
```

## Risiko-Level

| Level | Score | Beschreibung |
|---|---|---|
| `LOW` | 0–30 | Wahrscheinlich legitim |
| `MEDIUM` | 31–60 | Verdächtig, manuelle Prüfung empfohlen |
| `HIGH` | 61–100 | Sehr wahrscheinlich Fake/Wegwerf-Adresse |

## Anwendungsfälle

- **Registrierung:** Wegwerf-Adressen bei Account-Erstellung blockieren
- **Newsletter:** Listenhygiene — Fake-Adressen vor Versand aussortieren
- **Lead-Qualifizierung:** Nur Leads mit echten E-Mail-Adressen weiterverarbeiten
