# USt-ID Validierung — VAT Check

Validiert europäische Umsatzsteuer-Identifikationsnummern in mehreren Schichten: Format-Prüfung, Prüfziffer und VIES-Abfrage. Zusätzlich können EU-Steuersätze kostenlos abgerufen werden.

## Endpoints

```
POST https://api.paperoffice.ai/latest/vat/validate
GET  https://api.paperoffice.ai/latest/vat/rates    (GRATIS)
```

**Authentifizierung:** Bearer Token für `/vat/validate`. `/vat/rates` ist kostenlos ohne Token.

## Parameter (validate)

| Parameter | Typ | Pflicht | Beschreibung |
|---|---|---|---|
| `vat_id` | string | ✅ | USt-ID inkl. Länderkennung (z.B. `DE123456789`) |
| `ip` | string | ❌ | IP für zusätzliche Geo-Prüfung |
| `email` | string | ❌ | E-Mail für zusätzliche Plausibilitätsprüfung |
| `force_recheck` | bool | ❌ | Cache umgehen, direkt bei VIES prüfen |
| `geocoding` | bool | ❌ | Adress-Geocoding aktivieren |

## Ausführen

```bash
export PAPEROFFICE_API_KEY=po_sk_xxx

# Bash
bash example.sh "DE123456789"

# Python
pip install requests
python3 example.py "DE123456789"

# Node.js (v18+)
node example.js "DE123456789"
```

## Erwartete Antwort (validate)

```json
{
    "status": "error",
    "vat_id": "DE123456789",
    "format_valid": false,
    "error": "INVALID_CHECKSUM",
    "message": "Pruefziffer ungueltig",
    "layer": "L1_format"
}
```

## Erwartete Antwort (rates)

```json
{
    "DE": { "standard": 19, "reduced": 7 },
    "AT": { "standard": 20, "reduced": 10 },
    "FR": { "standard": 20, "reduced": 5.5 }
}
```

## Validierungs-Schichten

| Layer | Beschreibung |
|---|---|
| `L1_format` | Format- und Prüfziffervalidierung |
| `L2_vies` | VIES-Datenbankabfrage (EU-Kommission) |
| `L3_enrichment` | Adress-Abgleich, Geo-Prüfung |

## Anwendungsfälle

- **E-Commerce:** USt-ID bei Checkout validieren, korrekte Steuersätze anwenden
- **Rechnungserstellung:** Reverse-Charge-Verfahren automatisch anwenden
- **Compliance:** USt-ID-Prüfungen für Betriebsprüfung dokumentieren
