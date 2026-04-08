# Ausweisdokument-Extraktion (IDP Identity)

Extrahiert strukturierte Daten aus **Personalausweisen, Reisepässen und Führerscheinen** — Name, Geburtsdatum, Dokumentnummer, Ablaufdatum, Nationalität und mehr.

## Endpoint

```
POST https://api.paperoffice.ai/latest/job/add/workflow
```

**Authentifizierung:** Bearer Token (API-Key erforderlich)

## Parameter

| Parameter         | Wert       | Beschreibung                         |
|-------------------|------------|--------------------------------------|
| `file_1`          | Datei      | Scan oder Foto des Ausweises         |
| `model`           | `premium`  | Extraktionsqualität                  |
| `idp_collection`  | `identity` | Ausweisdokument-Extraktion aktivieren|
| `priority`        | `900`      | Synchrone Verarbeitung (≥900)        |

## Ausführen

```bash
export PAPEROFFICE_API_KEY="dein_api_key"

# Bash
bash example.sh ausweis.pdf

# Python
pip install requests
python3 example.py ausweis.pdf

# Node.js
npm install form-data
node example.js ausweis.pdf
```

## Verfügbare Ausweis-Felder

### Persönliche Daten

| Feld                     | Typ      | Beschreibung                         |
|--------------------------|----------|--------------------------------------|
| `_first_name`            | string   | Vorname                              |
| `_last_name`             | string   | Nachname                             |
| `_full_name`             | string   | Vollständiger Name                   |
| `_date_of_birth`         | date     | Geburtsdatum                         |
| `_place_of_birth`        | string   | Geburtsort                           |
| `_gender`                | string   | Geschlecht                           |
| `_nationality`           | string   | Staatsangehörigkeit                  |
| `_address`               | string   | Wohnadresse (falls vorhanden)        |

### Dokumentdaten

| Feld                     | Typ      | Beschreibung                         |
|--------------------------|----------|--------------------------------------|
| `_document_type`         | string   | Art (Personalausweis, Reisepass, Führerschein) |
| `_document_number`       | string   | Dokumentnummer / Seriennummer        |
| `_issuing_authority`     | string   | Ausstellende Behörde                 |
| `_issuing_country`       | string   | Ausstellungsland                     |
| `_issue_date`            | date     | Ausstellungsdatum                    |
| `_expiry_date`           | date     | Ablaufdatum / Gültig bis             |

### Maschinenlesbare Zone (MRZ)

| Feld                     | Typ      | Beschreibung                         |
|--------------------------|----------|--------------------------------------|
| `_mrz_line_1`            | string   | Erste Zeile der MRZ                  |
| `_mrz_line_2`            | string   | Zweite Zeile der MRZ                 |
| `_mrz_line_3`            | string   | Dritte Zeile der MRZ (falls vorhanden)|

## Response-Struktur

```json
{
  "status": "success",
  "job_id": "poai-job_900_...",
  "result": {
    "pages_idp": [{
      "suggested_fields": {
        "_full_name": {
          "type": "string",
          "value": "Max Mustermann",
          "source_boxes_confidence": "high"
        },
        "_document_number": {
          "type": "string",
          "value": "T220001293",
          "source_boxes_confidence": "high"
        },
        "_date_of_birth": {
          "type": "date",
          "value": "1985-03-15",
          "source_boxes_confidence": "high"
        },
        "_expiry_date": {
          "type": "date",
          "value": "2028-03-14",
          "source_boxes_confidence": "high"
        },
        "_nationality": {
          "type": "string",
          "value": "DEUTSCH",
          "source_boxes_confidence": "high"
        }
      }
    }]
  }
}
```

## Typische Anwendungsfälle

- **KYC-Prüfung**: Know Your Customer im Finanzsektor
- **Onboarding**: Automatische Datenerfassung bei Neukundenregistrierung
- **Altersverifikation**: Geburtsdatum automatisch prüfen
- **Ablaufüberwachung**: Dokumente mit ablaufender Gültigkeit erkennen

## Hinweis zum Datenschutz

Ausweisdokumente enthalten besonders schützenswerte personenbezogene Daten. Beachte:
- DSGVO-konforme Verarbeitung sicherstellen
- Daten nur so lange speichern wie nötig
- Zugriff auf extrahierte Daten beschränken
- PaperOffice AI verarbeitet Daten auf EU-Servern (Frankfurt)
