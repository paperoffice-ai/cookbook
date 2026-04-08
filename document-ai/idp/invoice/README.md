# Rechnungs-Extraktion (IDP Invoice)

Extrahiert **28+ strukturierte Felder** aus Rechnungen — Rechnungsnummer, Beträge, Lieferant, IBAN, Positionen und mehr. Jedes Feld enthält Konfidenz-Angaben und Bounding Boxes.

## Endpoint

```
POST https://api.paperoffice.ai/latest/job/add/workflow
```

**Authentifizierung:** Bearer Token (API-Key erforderlich)

## Parameter

| Parameter         | Wert       | Beschreibung                         |
|-------------------|------------|--------------------------------------|
| `file_1`          | Datei      | PDF oder Bild der Rechnung           |
| `model`           | `premium`  | Extraktionsqualität (basic/premium/ultra) |
| `idp_collection`  | `invoice`  | Rechnungs-Extraktion aktivieren      |
| `priority`        | `900`      | Synchrone Verarbeitung (≥900)        |

## Ausführen

```bash
export PAPEROFFICE_API_KEY="dein_api_key"

# Bash
bash example.sh rechnung.pdf

# Python
pip install requests
python3 example.py rechnung.pdf

# Node.js
npm install form-data
node example.js rechnung.pdf
```

## Verfügbare Rechnungsfelder

Die IDP-Engine extrahiert folgende Felder (Prefix `_`):

### Kopfdaten

| Feld                     | Typ      | Beschreibung                        |
|--------------------------|----------|-------------------------------------|
| `_invoice_number`        | string   | Rechnungsnummer                     |
| `_invoice_date`          | date     | Rechnungsdatum                      |
| `_invoice_due_date`      | date     | Fälligkeitsdatum                    |
| `_invoice_type`          | string   | Rechnungsart (Rechnung/Gutschrift)  |
| `_invoice_description`   | string   | Beschreibung / Betreff              |
| `_purchase_order_number` | string   | Bestellnummer                       |
| `_delivery_date`         | date     | Lieferdatum                         |

### Beträge

| Feld                     | Typ      | Beschreibung                        |
|--------------------------|----------|-------------------------------------|
| `_total_amount`          | number   | Gesamtbetrag (brutto)               |
| `_net_amount`            | number   | Nettobetrag                         |
| `_vat_amount`            | number   | Umsatzsteuer-Betrag                 |
| `_vat_rate`              | number   | USt-Satz in Prozent                 |
| `_discount_amount`       | number   | Rabatt-Betrag                       |
| `_currency`              | string   | Währung (EUR, USD, etc.)            |

### Lieferant (Kreditor)

| Feld                     | Typ      | Beschreibung                        |
|--------------------------|----------|-------------------------------------|
| `_supplier_name`         | string   | Firmenname des Lieferanten          |
| `_supplier_address`      | string   | Adresse des Lieferanten             |
| `_supplier_vat_id`       | string   | USt-IdNr. des Lieferanten           |
| `_supplier_tax_id`       | string   | Steuernummer des Lieferanten        |
| `_supplier_email`        | string   | E-Mail des Lieferanten              |
| `_supplier_phone`        | string   | Telefon des Lieferanten             |

### Kunde (Debitor)

| Feld                     | Typ      | Beschreibung                        |
|--------------------------|----------|-------------------------------------|
| `_customer_name`         | string   | Firmenname des Kunden               |
| `_customer_address`      | string   | Adresse des Kunden                  |
| `_customer_vat_id`       | string   | USt-IdNr. des Kunden                |
| `_customer_number`       | string   | Kundennummer                        |

### Bankverbindung

| Feld                     | Typ      | Beschreibung                        |
|--------------------------|----------|-------------------------------------|
| `_creditor_iban`         | string   | IBAN des Kreditors                  |
| `_creditor_bic`          | string   | BIC/SWIFT des Kreditors             |
| `_creditor_bank_name`    | string   | Bankname des Kreditors              |
| `_payment_reference`     | string   | Zahlungsreferenz / Verwendungszweck |
| `_payment_terms`         | string   | Zahlungsbedingungen                 |

### Positionen (Tabelle)

| Feld                     | Typ      | Beschreibung                        |
|--------------------------|----------|-------------------------------------|
| `_line_items`            | table    | Einzelpositionen der Rechnung       |

Die Tabelle `_line_items` kann pro Zeile enthalten: Beschreibung, Menge, Einzelpreis, Gesamtpreis, USt-Satz.

## Response-Struktur

```json
{
  "status": "success",
  "job_id": "poai-job_900_...",
  "operation": "document_idp",
  "pipeline": "workflow",
  "result": {
    "pages_idp": [{
      "document_information": { "total_pages": 1 },
      "suggested_fields": {
        "_invoice_number": {
          "type": "string",
          "value": "2024-001",
          "value_raw": "2024-001",
          "source_boxes": [0],
          "source_boxes_confidence": "high"
        },
        "_total_amount": {
          "type": "number",
          "value": "1.469,06",
          "value_raw": "1469.06",
          "source_boxes_confidence": "high"
        }
      }
    }]
  }
}
```

## Feld-Metadaten

Jedes Feld enthält:

| Eigenschaft               | Beschreibung                              |
|---------------------------|-------------------------------------------|
| `type`                    | Datentyp (string, number, date, table)    |
| `value`                   | Formatierter Wert (z.B. "1.469,06")      |
| `value_raw`               | Rohwert für Weiterverarbeitung ("1469.06")|
| `source_boxes`            | Positionen im Dokument (Bounding Boxes)   |
| `source_boxes_confidence` | Konfidenz: high, medium, low              |

## Tipps

- **`value_raw`** für numerische Weiterverarbeitung nutzen (Punkt als Dezimaltrenner)
- **`source_boxes_confidence`** bei "low" → manuelles Review empfohlen
- **`model=ultra`** für komplexe mehrseitige Rechnungen mit vielen Positionen
