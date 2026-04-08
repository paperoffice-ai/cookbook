#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════
# PaperOffice AI — Invoice Extractor mit Bounding Boxes
# Bearer Token ERFORDERLICH
# ═══════════════════════════════════════════════════════════════

set -euo pipefail

API_KEY="${PAPEROFFICE_API_KEY:?Bitte PAPEROFFICE_API_KEY setzen (export PAPEROFFICE_API_KEY=po_sk_xxx)}"
INPUT_FILE="${1:-invoice.pdf}"

if [ ! -f "$INPUT_FILE" ]; then
  echo "Verwendung: $0 <pdf-datei>"
  echo "Beispiel:   $0 invoice.pdf"
  exit 1
fi

echo "→ Extrahiere Rechnungsdaten aus: $INPUT_FILE"

curl -s -X POST "https://api.paperoffice.ai/latest/job" \
  -H "Authorization: Bearer ${API_KEY}" \
  -F "file_1=@${INPUT_FILE}" \
  -F "model=premium" \
  -F "idp_collection=invoice" \
  -F "priority=900" | python3 -m json.tool

# Response enthält Bounding Boxes pro Feld:
# → "vendor": {"value": "Acme Corp", "bbox": [x1, y1, x2, y2]}
