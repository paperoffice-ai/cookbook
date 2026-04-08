# PDF Merge — Mehrere PDFs zusammenfügen

Fügt beliebig viele PDF-Dateien zu einem einzelnen Dokument zusammen. Die Reihenfolge der Eingabedateien bestimmt die Seitenreihenfolge im Ergebnis.

## Endpoint

```
POST https://api.paperoffice.ai/latest/job/add/workflow
```

**Authentifizierung:** Bearer Token (API-Key erforderlich)

## Parameter

| Parameter         | Wert          | Beschreibung                             |
|-------------------|---------------|------------------------------------------|
| `file_1`          | Datei         | Erste PDF-Datei                          |
| `file_2`          | Datei         | Zweite PDF-Datei                         |
| `file_N`          | Datei         | Weitere PDFs (beliebig viele)            |
| `template`        | `pdf_merge`   | Workflow-Template für Merge              |
| `output_filename` | Text          | Dateiname der zusammengefügten PDF       |
| `priority`        | `900`         | Synchrone Verarbeitung (≥900 = sofort)   |

## Ausführen

```bash
export PAPEROFFICE_API_KEY="dein_api_key"

# Bash
chmod +x example.sh && ./example.sh datei1.pdf datei2.pdf

# Python
pip install requests
python3 example.py datei1.pdf datei2.pdf datei3.pdf

# Node.js (v18+)
node example.js datei1.pdf datei2.pdf
```

## Response-Struktur

```json
{
  "status": "success",
  "job_id": "poai-job_900_...",
  "operation": "pdf_merge",
  "result": {
    "files": [
      "https://api.paperoffice.ai/latest/job/download/ZBVXGX9A..."
    ],
    "duration_ms": 1200
  }
}
```

## Download des Ergebnisses

Die Download-URL steht in `result.files[0]`:

```bash
curl -s "https://api.paperoffice.ai/latest/job/download/ZBVXGX9A..." \
  -H "Authorization: Bearer ${PAPEROFFICE_API_KEY}" \
  -o "merged.pdf"
```

## Typische Anwendungsfälle

- **Rechnungspaket erstellen** — Rechnung + AGB + Lieferschein in ein PDF
- **Bewerbungsmappe** — Anschreiben + Lebenslauf + Zeugnisse zusammenfügen
- **Vertragsunterlagen** — Vertrag + Anlagen + Unterschriftenblatt bündeln
- **Archivierung** — Zusammengehörige Dokumente als ein Paket speichern

## Siehe auch

- [PDF AI Split](../ai-split/) — PDF intelligent in Teile splitten
- [PDF Convert](../convert/) — PDF in andere Formate konvertieren
- [PDF Anonymize](../anonymize/) — DSGVO-konforme Anonymisierung
