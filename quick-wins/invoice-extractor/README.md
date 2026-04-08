# Invoice Extractor mit Bounding Boxes

Extrahiert Rechnungsfelder (Lieferant, Betrag, Datum, IBAN etc.) aus PDFs — inklusive **Bounding Boxes** die zeigen, *wo* der Wert im Dokument steht.

## Voraussetzungen

Ein PaperOffice API-Key ist erforderlich. Erhältlich unter [paperoffice.ai](https://paperoffice.ai).

```bash
export PAPEROFFICE_API_KEY=po_sk_xxx
```

## Quick Start

```bash
# cURL
bash example.sh invoice.pdf

# Python
pip install requests
python example.py invoice.pdf

# Node.js
npm install form-data
node example.js invoice.pdf
```

## Was sind Source Boxes?

Jedes extrahierte Feld enthält `source_boxes` mit Positionen im Dokument. Perfekt für:
- Verification UI (Feld im PDF highlighten)
- Confidence-Checks (`source_boxes_confidence`: high/medium/low → manuelles Review)
- Audit Trail (nachvollziehbar, woher der Wert stammt)

IDP-Felder nutzen `_`-Prefix: `_invoice_number`, `_total_amount`, `_supplier_name`, etc.

## API-Details

| Parameter | Wert | Beschreibung |
|---|---|---|
| `Authorization` | `Bearer po_sk_xxx` | **Erforderlich** |
| `file_1` | PDF/Bild | Hochzuladende Datei |
| `model` | `premium` | Höchste Extraktionsqualität |
| `idp_collection` | `invoice` | Rechnungs-Extraktion |
| `priority` | `900` | Synchrone Antwort (≥900) |
