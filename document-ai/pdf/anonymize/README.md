# PDF Anonymize — DSGVO-konforme Anonymisierung

Anonymisiert personenbezogene Daten in PDF-Dokumenten automatisch. Die KI erkennt sensible Informationen und schwärzt diese DSGVO-konform — ideal für Datenweitergabe, Archivierung oder Auskunftsersuchen.

## Endpoint

```
POST https://api.paperoffice.ai/latest/job/add/workflow
```

**Authentifizierung:** Bearer Token (API-Key erforderlich)

## Parameter

| Parameter          | Wert              | Beschreibung                                |
|--------------------|-------------------|---------------------------------------------|
| `file_1`           | Datei             | Das zu anonymisierende PDF                  |
| `template`         | `pdf_anonymize`   | Workflow-Template für Anonymisierung        |
| `anonymize_fields` | Text (optional)   | Kommaseparierte Liste zu schwärzender Felder|
| `priority`         | `900`             | Synchrone Verarbeitung (≥900 = sofort)      |

## Erkannte Datentypen

Die KI erkennt und schwärzt automatisch:

| Kategorie             | Beispiele                                    |
|-----------------------|----------------------------------------------|
| **Personennamen**     | Vor- und Nachnamen, Firmenverantwortliche    |
| **Adressen**          | Straße, PLZ, Stadt, Land                     |
| **Kontaktdaten**      | Telefon, E-Mail, Fax                         |
| **Finanzdaten**       | IBAN, BIC, Kontonummern, Kreditkarten        |
| **Identifikation**    | Steuernummer, Personalausweis, Sozialvers.   |
| **Geburtsdaten**      | Geburtsdatum, Geburtsort                     |

## anonymize_fields — Gezielte Anonymisierung

Ohne `anonymize_fields` werden alle erkannten personenbezogenen Daten geschwärzt. Mit dem Parameter kann die Anonymisierung auf bestimmte Felder eingeschränkt werden:

```bash
# Nur Namen und Adressen schwärzen
-F "anonymize_fields=name,adresse"

# Nur Finanzdaten schwärzen
-F "anonymize_fields=iban,kontonummer,kreditkarte"

# Nur Kontaktdaten schwärzen
-F "anonymize_fields=email,telefon"
```

## Ausführen

```bash
export PAPEROFFICE_API_KEY="dein_api_key"

# Bash — Alle personenbezogenen Daten schwärzen
chmod +x example.sh && ./example.sh dokument.pdf

# Python — Alle Daten schwärzen
pip install requests
python3 example.py dokument.pdf

# Python — Nur bestimmte Felder
python3 example.py dokument.pdf "name,adresse,iban"

# Node.js (v18+)
node example.js dokument.pdf
node example.js dokument.pdf "name,email,telefon"
```

## Response-Struktur

```json
{
  "status": "success",
  "job_id": "poai-job_900_...",
  "result": {
    "status": "completed",
    "output_files": [
      {
        "filename": "dokument_anonymisiert.pdf",
        "download_token": "dl_abc123..."
      }
    ]
  }
}
```

## Download des Ergebnisses

```
GET https://api.paperoffice.ai/latest/job/download/{download_token}
```

## DSGVO-Konformität

- **Art. 17 DSGVO** — Recht auf Löschung: Anonymisierte Dokumente enthalten keine personenbezogenen Daten mehr
- **Art. 15 DSGVO** — Auskunftsrecht: Dokumente vor Weitergabe anonymisieren
- **Art. 25 DSGVO** — Datenschutz durch Technikgestaltung: Automatische Schwärzung als technische Maßnahme
- **Revisionssicher** — Die Schwärzung ist permanent, nicht rückgängig machbar

## Typische Anwendungsfälle

- **Auskunftsersuchen** — Dokumente an Dritte weitergeben ohne personenbezogene Daten
- **Testdaten erzeugen** — Produktionsdokumente für Test/Entwicklung anonymisieren
- **Archivierung** — Aufbewahrungspflichtige Dokumente nach Ablauf der Personenbezugs-Frist schwärzen
- **Weitergabe an Externe** — Verträge, Rechnungen anonymisiert an Berater/Prüfer senden

## Siehe auch

- [PDF AI Split](../ai-split/) — PDF intelligent in Teile splitten
- [PDF Merge](../merge/) — Mehrere PDFs zusammenfügen
- [PDF Convert](../convert/) — PDF in andere Formate konvertieren
