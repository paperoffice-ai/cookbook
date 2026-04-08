# Batch OCR → CSV Export

Verarbeitet einen Ordner voller Dokumente (PDF, PNG, JPG, TIFF, WebP) per OCR und exportiert die Ergebnisse als CSV.

## Voraussetzungen

```bash
export PAPEROFFICE_API_KEY=po_sk_xxx
pip install requests
```

## Verwendung

```bash
python pipeline.py ./documents                    # → ocr_results.csv
python pipeline.py ./scans ergebnisse.csv         # → ergebnisse.csv
```

## Output CSV

| Spalte | Beschreibung |
|---|---|
| `filename` | Dateiname |
| `pages` | Seitenanzahl |
| `text_length` | Anzahl Zeichen |
| `text_preview` | Erste 500 Zeichen |
| `confidence` | OCR-Confidence |

## Unterstützte Formate

PDF, PNG, JPG/JPEG, TIFF, WebP
