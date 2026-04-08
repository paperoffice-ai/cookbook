# Vertragsanalyse (IDP Contract)

Extrahiert strukturierte Daten aus **Verträgen** — Vertragsparteien, Laufzeit, Kündigungsfrist, Vertragswert und Schlüsselklauseln.

## Endpoint

```
POST https://api.paperoffice.ai/latest/job/add/workflow
```

**Authentifizierung:** Bearer Token (API-Key erforderlich)

## Parameter

| Parameter         | Wert       | Beschreibung                         |
|-------------------|------------|--------------------------------------|
| `file_1`          | Datei      | PDF des Vertrags                     |
| `model`           | `premium`  | Extraktionsqualität                  |
| `idp_collection`  | `contract` | Vertragsanalyse aktivieren           |
| `priority`        | `900`      | Synchrone Verarbeitung (≥900)        |

## Ausführen

```bash
export PAPEROFFICE_API_KEY="dein_api_key"

# Bash
bash example.sh vertrag.pdf

# Python
pip install requests
python3 example.py vertrag.pdf

# Node.js
npm install form-data
node example.js vertrag.pdf
```

## Verfügbare Vertragsfelder

### Vertragsparteien

| Feld                     | Typ      | Beschreibung                         |
|--------------------------|----------|--------------------------------------|
| `_party_a_name`          | string   | Name / Firma der ersten Partei       |
| `_party_a_address`       | string   | Adresse der ersten Partei            |
| `_party_b_name`          | string   | Name / Firma der zweiten Partei      |
| `_party_b_address`       | string   | Adresse der zweiten Partei           |

### Vertragsdaten

| Feld                     | Typ      | Beschreibung                         |
|--------------------------|----------|--------------------------------------|
| `_contract_type`         | string   | Vertragsart (Mietvertrag, Dienstvertrag, etc.) |
| `_contract_number`       | string   | Vertragsnummer / Aktenzeichen        |
| `_contract_date`         | date     | Datum des Vertragsabschlusses        |
| `_effective_date`        | date     | Inkrafttreten des Vertrags           |

### Laufzeit & Kündigung

| Feld                     | Typ      | Beschreibung                         |
|--------------------------|----------|--------------------------------------|
| `_start_date`            | date     | Vertragsbeginn                       |
| `_end_date`              | date     | Vertragsende                         |
| `_duration`              | string   | Laufzeit (z.B. "24 Monate")         |
| `_notice_period`         | string   | Kündigungsfrist                      |
| `_renewal_clause`        | string   | Automatische Verlängerung            |

### Finanzielles

| Feld                     | Typ      | Beschreibung                         |
|--------------------------|----------|--------------------------------------|
| `_contract_value`        | number   | Vertragswert / Gesamtsumme          |
| `_monthly_payment`       | number   | Monatliche Zahlung                   |
| `_payment_terms`         | string   | Zahlungsbedingungen                  |
| `_currency`              | string   | Währung                              |

### Weitere Klauseln

| Feld                     | Typ      | Beschreibung                         |
|--------------------------|----------|--------------------------------------|
| `_governing_law`         | string   | Anwendbares Recht / Gerichtsstand    |
| `_confidentiality`       | string   | Vertraulichkeitsklausel              |
| `_penalty_clause`        | string   | Vertragsstrafe                       |

## Response-Struktur

```json
{
  "status": "success",
  "job_id": "poai-job_900_...",
  "result": {
    "pages_idp": [{
      "suggested_fields": {
        "_party_a_name": {
          "type": "string",
          "value": "Mustermann GmbH",
          "source_boxes_confidence": "high"
        },
        "_duration": {
          "type": "string",
          "value": "24 Monate",
          "source_boxes_confidence": "high"
        },
        "_notice_period": {
          "type": "string",
          "value": "3 Monate zum Quartalsende",
          "source_boxes_confidence": "medium"
        }
      }
    }]
  }
}
```

## Tipps

- **`model=ultra`** für mehrseitige Verträge mit komplexen Klauseln empfohlen
- Kombiniere mit **Custom Fields** (`idp_fields`) für branchenspezifische Klauseln
- Bei niedrigem `source_boxes_confidence` → manuelles Review einplanen
