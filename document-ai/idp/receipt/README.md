# Kassenbon-Extraktion (IDP Receipt)

Extrahiert strukturierte Daten aus **Kassenbons und Quittungen** — Geschäftsname, Betrag, Datum, Zahlungsmethode und Artikelpositionen.

## Endpoint

```
POST https://api.paperoffice.ai/latest/job/add/workflow
```

**Authentifizierung:** Bearer Token (API-Key erforderlich)

## Parameter

| Parameter         | Wert       | Beschreibung                         |
|-------------------|------------|--------------------------------------|
| `file_1`          | Datei      | Foto oder Scan des Kassenbons        |
| `model`           | `premium`  | Extraktionsqualität                  |
| `idp_collection`  | `receipt`  | Kassenbon-Extraktion aktivieren      |
| `priority`        | `900`      | Synchrone Verarbeitung (≥900)        |

## Ausführen

```bash
export PAPEROFFICE_API_KEY="dein_api_key"

# Bash
bash example.sh kassenbon.pdf

# Python
pip install requests
python3 example.py kassenbon.pdf

# Node.js
npm install form-data
node example.js kassenbon.pdf
```

## Verfügbare Kassenbon-Felder

| Feld                     | Typ      | Beschreibung                         |
|--------------------------|----------|--------------------------------------|
| `_store_name`            | string   | Geschäftsname / Filiale              |
| `_store_address`         | string   | Adresse des Geschäfts                |
| `_store_phone`           | string   | Telefonnummer                        |
| `_receipt_date`          | date     | Datum des Einkaufs                   |
| `_receipt_time`          | string   | Uhrzeit des Einkaufs                 |
| `_receipt_number`        | string   | Bonnummer / Transaktionsnummer       |
| `_total_amount`          | number   | Gesamtbetrag                         |
| `_net_amount`            | number   | Nettobetrag                          |
| `_vat_amount`            | number   | Umsatzsteuer-Betrag                  |
| `_vat_rate`              | number   | USt-Satz                             |
| `_payment_method`        | string   | Zahlungsmethode (Bar, Karte, etc.)   |
| `_card_last_four`        | string   | Letzte 4 Ziffern der Karte           |
| `_currency`              | string   | Währung                              |
| `_cashier`               | string   | Kassiererin / Bedienung              |
| `_line_items`            | table    | Einzelne Artikelpositionen           |

## Response-Struktur

```json
{
  "status": "success",
  "job_id": "poai-job_900_...",
  "result": {
    "pages_idp": [{
      "suggested_fields": {
        "_store_name": {
          "type": "string",
          "value": "REWE Markt GmbH",
          "source_boxes_confidence": "high"
        },
        "_total_amount": {
          "type": "number",
          "value": "23,47",
          "value_raw": "23.47",
          "source_boxes_confidence": "high"
        },
        "_payment_method": {
          "type": "string",
          "value": "EC-Karte",
          "source_boxes_confidence": "high"
        }
      }
    }]
  }
}
```

## Typische Anwendungsfälle

- **Spesenabrechnung**: Automatische Erfassung von Belegen
- **Buchhaltung**: Belegerfassung für Kleinbeträge
- **Reisekostenabrechnung**: Hotel- und Restaurantquittungen
- **Ausgabenverfolgung**: Persönliche oder geschäftliche Ausgaben kategorisieren
