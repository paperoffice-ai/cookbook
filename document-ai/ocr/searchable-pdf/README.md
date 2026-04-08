# Searchable PDF — Durchsuchbare PDF aus Scans erzeugen

Verwandle gescannte PDFs und Bilder in durchsuchbare PDFs mit unsichtbarer Textschicht. Ideal für die Archivierung — das Originaldokument bleibt visuell unverändert, ist aber volltextdurchsuchbar.

## Endpoint

```
POST https://api.paperoffice.ai/latest/job/add/paperoffice_aiocr___generate
```

**Authentifizierung:** Bearer Token (API-Key erforderlich)

## Parameter

| Parameter               | Wert   | Beschreibung                              |
|------------------------|--------|-------------------------------------------|
| `file_1`               | Datei  | Das zu verarbeitende Dokument             |
| `ocr_mode`             | `text` | Text-Extraktion als Basis                 |
| `output_searchable_pdf`| `true` | Durchsuchbare PDF zusätzlich erzeugen     |
| `priority`             | `900`  | Synchrone Verarbeitung (sofort)           |

## Ausführen

```bash
export PAPEROFFICE_API_KEY="dein_api_key"

# Bash — Ergebnis wird als searchable_output.pdf gespeichert
chmod +x example.sh && ./example.sh /pfad/zur/datei.pdf

# Bash — mit eigenem Ausgabepfad
./example.sh /pfad/zur/datei.pdf /pfad/zur/ausgabe.pdf

# Python
pip install requests
python3 example.py /pfad/zur/datei.pdf ausgabe.pdf

# Node.js (v18+)
node example.js /pfad/zur/datei.pdf ausgabe.pdf
```

## Wann Searchable PDF verwenden?

- **Archivierung** — GoBD/DSGVO-konforme Langzeitarchivierung mit Volltextsuche
- **DMS-Import** — Dokumente durchsuchbar ins DMS einpflegen
- **Compliance** — Originallayout beibehalten, gleichzeitig durchsuchbar machen
- **Scan-Nachbearbeitung** — Papier-Scans für digitale Workflows aufbereiten

## Response-Struktur

Die Response enthält sowohl den extrahierten Text als auch einen Download-Link für die durchsuchbare PDF:

```json
{
  "status": "success",
  "job_id": "poai-job_900_...",
  "result": {
    "status": "completed",
    "output": {
      "pages": {
        "00001": {
          "ocr_text": "Text der Seite...",
          "confidence_avg": 0.9954
        }
      },
      "ocr_mode": "text",
      "searchable_pdf_url": "https://api.paperoffice.ai/latest/job/download/...",
      "download_token": "abc123...",
      "summary": {
        "total_pages": 1,
        "avg_confidence": 1,
        "poaiocr_extracted_fulltext": "***Page 1 of 1***\n\nDer extrahierte Text...",
        "processing_engine": "paperoffice_ai_ocr_neural_v3.0"
      }
    },
    "duration_ms": "892.31"
  }
}
```

## Zusätzliche Felder

| Feld | Beschreibung |
|------|-------------|
| `output.searchable_pdf_url` | Direkte Download-URL für die durchsuchbare PDF |
| `output.download_token` | Alternativ: Token für Download über `/job/download/{token}` |

## Workflow: Scan → Archiv

```
1. Scan hochladen (file_1)
2. OCR + Searchable PDF erzeugen (output_searchable_pdf=true)
3. Durchsuchbare PDF herunterladen
4. Im DMS/Archiv ablegen → Volltextsuche funktioniert sofort
```

## Siehe auch

- [Text-Mode](../text-mode/) — Nur reiner Text (ohne PDF-Erzeugung)
- [Complete-Mode](../complete-mode/) — Text + Bounding Boxes + Tabellen
