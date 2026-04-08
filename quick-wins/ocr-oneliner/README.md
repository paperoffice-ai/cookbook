# OCR One-Liner

Text aus Bildern und PDFs extrahieren — ein einziger API-Call.

## Voraussetzungen

```bash
export PAPEROFFICE_API_KEY=po_sk_xxx
```

## Quick Start

```bash
# cURL
bash example.sh scan.png

# Python
pip install requests
python example.py scan.png

# Node.js
npm install form-data
node example.js scan.png
```

## OCR-Modi

| Modus | Beschreibung |
|---|---|
| `complete` | Text + Tabellen-Erkennung |
| `grid` | Nur Bounding Boxes (Position jedes Wortes) |
| `text` | Nur Fließtext |

## API-Details

| Parameter | Wert | Beschreibung |
|---|---|---|
| `Authorization` | `Bearer po_sk_xxx` | **Erforderlich** |
| `file_1` | PDF/PNG/JPG/TIFF/WebP | Hochzuladende Datei |
| `ocr_mode` | `complete` | Erkennungsmodus |
| `priority` | `900` | Synchrone Antwort (≥900) |
