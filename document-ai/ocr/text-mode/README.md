# OCR Text-Mode — Reiner Text, schnellster Modus

Extrahiere reinen Text aus PDFs, Bildern oder Scans. Der Text-Mode ist der schnellste OCR-Modus — ideal wenn nur der Textinhalt benötigt wird, ohne Layout- oder Positionsdaten.

## Endpoint

```
POST https://api.paperoffice.ai/latest/job/add/paperoffice_aiocr___generate
```

**Authentifizierung:** Bearer Token (API-Key erforderlich)

## Parameter

| Parameter  | Wert     | Beschreibung                          |
|-----------|----------|---------------------------------------|
| `file_1`  | Datei    | Das zu verarbeitende Dokument         |
| `ocr_mode`| `text`   | Nur reinen Text extrahieren           |
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

## Wann Text-Mode verwenden?

- **Volltextsuche** — Index für Suchmaschinen aufbauen
- **KI-Verarbeitung** — Text als Input für LLMs oder Embeddings
- **Schnelle Extraktion** — Wenn Layout/Position irrelevant ist
- **Batch-Verarbeitung** — Hoher Durchsatz bei vielen Dokumenten

## Response-Struktur

```json
{
  "status": "success",
  "job_id": "poai-job_900_...",
  "result": {
    "status": "completed",
    "output": {
      "pages": {
        "00001": {
          "ocr_text": "Text der ersten Seite...",
          "line_count": 8,
          "confidence_avg": 0.9954,
          "char_count": 212,
          "language": { "primary": "de", "confidence": 0.95 }
        }
      },
      "ocr_mode": "text",
      "summary": {
        "total_pages": 1,
        "total_lines": 8,
        "total_chars": 212,
        "avg_confidence": 1,
        "poaiocr_extracted_fulltext": "***Page 1 of 1***\n\nDer vollständige Text...",
        "processing_engine": "paperoffice_ai_ocr_neural_v3.0"
      }
    },
    "duration_ms": "601.71"
  }
}
```

## Wichtige Felder

| Feld | Beschreibung |
|------|-------------|
| `summary.poaiocr_extracted_fulltext` | Gesamter Text aller Seiten (mit Seitenmarkern) |
| `pages.XXXXX.ocr_text` | Text einer einzelnen Seite |
| `pages.XXXXX.confidence_avg` | Erkennungssicherheit (0–1) |
| `summary.avg_confidence` | Durchschnittliche Konfidenz über alle Seiten |
| `summary.processing_engine` | Verwendete OCR-Engine |

## Siehe auch

- [Complete-Mode](../complete-mode/) — Text + Bounding Boxes + Tabellen
- [Searchable PDF](../searchable-pdf/) — Durchsuchbare PDF erzeugen
