# PDF Convert — PDF in andere Formate konvertieren

Konvertiert PDF-Dateien in verschiedene Zielformate. Layout, Tabellen und Formatierungen werden dabei bestmöglich beibehalten.

## Endpoint

```
POST https://api.paperoffice.ai/latest/job/add/workflow
```

**Authentifizierung:** Bearer Token (API-Key erforderlich)

## Parameter

| Parameter       | Wert           | Beschreibung                           |
|-----------------|----------------|----------------------------------------|
| `file_1`        | Datei          | Die zu konvertierende PDF              |
| `template`      | `pdf_convert`  | Workflow-Template für Konvertierung    |
| `target_format` | Text           | Zielformat (siehe unterstützte Formate)|
| `priority`      | `900`          | Synchrone Verarbeitung (≥900 = sofort) |

## Unterstützte Zielformate

| Format | Beschreibung                        | Typischer Einsatz                    |
|--------|-------------------------------------|--------------------------------------|
| `docx` | Microsoft Word                      | Bearbeitung von Textdokumenten       |
| `xlsx` | Microsoft Excel                     | Tabellen und Finanzdaten             |
| `pptx` | Microsoft PowerPoint                | Präsentationen                       |
| `html` | Webseite                            | Online-Anzeige, E-Mail-Einbettung    |
| `txt`  | Reiner Text                         | Weiterverarbeitung, KI-Input         |
| `jpg`  | JPEG-Bild                           | Vorschaubilder, Thumbnails           |
| `png`  | PNG-Bild                            | Hochwertige Bildausgabe              |

## Ausführen

```bash
export PAPEROFFICE_API_KEY="dein_api_key"

# Bash — Standard: docx
chmod +x example.sh && ./example.sh dokument.pdf

# Bash — Explizites Format
./example.sh dokument.pdf xlsx

# Python
pip install requests
python3 example.py dokument.pdf docx

# Node.js (v18+)
node example.js dokument.pdf html
```

## Response-Struktur

```json
{
  "status": "success",
  "job_id": "poai-job_900_...",
  "operation": "pdf_convert",
  "result": {
    "files": [
      "https://api.paperoffice.ai/latest/job/download/ZBVXGX9A..."
    ],
    "duration_ms": 2300
  }
}
```

## Download des Ergebnisses

Die Download-URL steht in `result.files[0]`:

```bash
curl -s "https://api.paperoffice.ai/latest/job/download/ZBVXGX9A..." \
  -H "Authorization: Bearer ${PAPEROFFICE_API_KEY}" \
  -o "ergebnis.docx"
```

## Typische Anwendungsfälle

- **Verträge bearbeiten** — PDF → DOCX zum Bearbeiten in Word
- **Finanzdaten extrahieren** — PDF-Tabellen → XLSX für Excel-Analyse
- **Web-Vorschau** — PDF → HTML für Browser-Darstellung
- **KI-Verarbeitung** — PDF → TXT als Input für Sprachmodelle
- **Bildexport** — PDF-Seiten → JPG/PNG für Vorschauen

## Siehe auch

- [PDF AI Split](../ai-split/) — PDF intelligent in Teile splitten
- [PDF Merge](../merge/) — Mehrere PDFs zusammenfügen
- [PDF Anonymize](../anonymize/) — DSGVO-konforme Anonymisierung
