# OCR Complete-Mode — Text + Bounding Boxes + Tabellen

Extrahiere Text inklusive Positionsdaten (Bounding Boxes), Tabellen-Strukturen und Layout-Informationen. Der Complete-Mode liefert alle verfügbaren OCR-Daten — ideal für Dokumentenanalyse mit Positionsbezug.

## Endpoint

```
POST https://api.paperoffice.ai/latest/job/add/paperoffice_aiocr___generate
```

**Authentifizierung:** Bearer Token (API-Key erforderlich)

## Parameter

| Parameter  | Wert       | Beschreibung                                 |
|-----------|------------|----------------------------------------------|
| `file_1`  | Datei      | Das zu verarbeitende Dokument                |
| `ocr_mode`| `complete` | Vollständige Analyse mit Layout + Tabellen   |
| `priority`| `900`      | Synchrone Verarbeitung (sofort)              |

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

## Wann Complete-Mode verwenden?

- **Tabellen-Extraktion** — Rechnungspositionen, Preislisten, Finanzdaten
- **Layout-Analyse** — Position von Textblöcken auf der Seite
- **Formular-Erkennung** — Felder mit ihren Koordinaten identifizieren
- **Dokumenten-Rekonstruktion** — Originalstruktur nachbilden

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
          "ocr_text": "Text der Seite...",
          "line_count": 12,
          "confidence_avg": 0.9871,
          "char_count": 456,
          "language": { "primary": "de", "confidence": 0.97 },
          "bounding_boxes": [
            {
              "text": "Rechnung #2024-001",
              "x": 50, "y": 80, "w": 320, "h": 28,
              "confidence": 0.99
            }
          ],
          "tables": [
            {
              "rows": [
                ["Pos", "Beschreibung", "Menge", "Preis"],
                ["1", "Beratung", "8h", "960,00 €"]
              ]
            }
          ]
        }
      },
      "ocr_tier": "complete",
      "ocr_mode": "complete",
      "summary": {
        "total_pages": 1,
        "total_lines": 12,
        "total_chars": 456,
        "avg_confidence": 0.99,
        "poaiocr_extracted_fulltext": "***Page 1 of 1***\n\nRechnung #2024-001...",
        "processing_engine": "paperoffice_ai_ocr_neural_v3.0"
      }
    },
    "duration_ms": "1203.44"
  }
}
```

## Zusätzliche Felder gegenüber Text-Mode

| Feld | Beschreibung |
|------|-------------|
| `pages.XXXXX.bounding_boxes` | Array mit Textblöcken inkl. Position (x, y, w, h) und Konfidenz |
| `pages.XXXXX.tables` | Erkannte Tabellen als verschachtelte Arrays |
| `ocr_tier` | Verwendeter OCR-Tier (`complete`) |

## Bounding-Box-Format

Jede Bounding Box enthält:

| Feld | Typ | Beschreibung |
|------|-----|-------------|
| `text` | string | Erkannter Text im Bereich |
| `x`, `y` | number | Position (links oben, in Pixel) |
| `w`, `h` | number | Breite und Höhe (in Pixel) |
| `confidence` | number | Erkennungssicherheit (0–1) |

## Siehe auch

- [Text-Mode](../text-mode/) — Nur reiner Text (schneller)
- [Searchable PDF](../searchable-pdf/) — Durchsuchbare PDF erzeugen
