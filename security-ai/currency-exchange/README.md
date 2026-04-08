# Währungsumrechnung — Currency Exchange

Ruft aktuelle Wechselkurse für 172+ Währungen ab. Unterstützt Umrechnung von und zu beliebigen ISO-4217-Währungen mit optionalem Betrag.

## Endpoint

```
POST https://api.paperoffice.ai/latest/currency_exchange/get_rates
```

**Authentifizierung:** VISITOR-fähig (kein Token nötig, aber IP-Ratelimit). Mit Bearer Token kein Limit.

## Parameter

| Parameter | Typ | Pflicht | Beschreibung |
|---|---|---|---|
| `from` | string | ✅ | Ausgangswährung (ISO 4217, z.B. `EUR`) |
| `to` | string | ❌ | Zielwährung (ohne = alle 172+ Währungen) |
| `amount` | float | ❌ | Umzurechnender Betrag (Standard: `1`) |

## Ausführen

```bash
# Kein Token nötig!

# Bash — 100 EUR in alle Währungen
bash example.sh EUR "" 100

# Bash — EUR nach USD
bash example.sh EUR USD 250

# Python
pip install requests
python3 example.py EUR USD 100

# Node.js (v18+)
node example.js EUR USD 100
```

## Erwartete Antwort

```json
{
    "base": "EUR",
    "amount": 100,
    "rates": {
        "USD": 115.86,
        "GBP": 86.12,
        "CHF": 95.43,
        "JPY": 16234.50
    },
    "currencies_count": 172
}
```

## Anwendungsfälle

- **E-Commerce:** Preise in lokaler Währung des Kunden anzeigen
- **Rechnungsstellung:** Internationale Rechnungen automatisch umrechnen
- **Finanz-Dashboards:** Live-Wechselkurse in Übersichten einbetten
- **Reisekosten:** Spesenabrechnungen in Heimatwährung konvertieren
