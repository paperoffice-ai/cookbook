# Erster OCR-Call — Text-Extraktion

Extrahiere Text aus einem Dokument (PDF, Bild, Scan) mit PaperOffice AI OCR.

## Endpoint

```
POST https://api.paperoffice.ai/latest/job/add/paperoffice_aiocr___generate
```

**Authentifizierung:** Bearer Token (API-Key erforderlich)

## Parameter

| Parameter  | Wert     | Beschreibung                          |
|-----------|----------|---------------------------------------|
| `file_1`  | Datei    | Das zu verarbeitende Dokument         |
| `ocr_mode`| `text`   | Nur Text extrahieren (kein Layout)    |
| `priority`| `900`    | Synchrone Verarbeitung (sofort)       |

## Ausführen

```bash
export PAPEROFFICE_API_KEY="dein_api_key"

# Bash
chmod +x example.sh && ./example.sh /pfad/zur/datei.pdf

# Python
pip install requests
python3 example.py /pfad/zur/datei.pdf

# Node.js (v18+)
node example.js /pfad/zur/datei.pdf
```

## Response-Struktur

```json
{
  "result": {
    "output": {
      "summary": {
        "poaiocr_extracted_fulltext": "Der vollständige extrahierte Text...",
        "total_pages": 1,
        "total_lines": 42,
        "avg_confidence": 0.97
      },
      "pages": {
        "00001": {
          "ocr_text": "Text der ersten Seite..."
        }
      }
    }
  }
}
```

## Priority-System

| Priority | Verhalten                                      |
|---------|------------------------------------------------|
| `900`   | **Synchron** — Ergebnis direkt in der Response  |
| `500`   | **Async** — Gibt `job_id` zurück zum Pollen     |
| `100`   | **Niedrig** — Hintergrund-Verarbeitung          |

Für synchrone Ergebnisse (wie in diesem Beispiel) immer `priority=900` verwenden.
