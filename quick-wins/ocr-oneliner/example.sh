#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════
# PaperOffice AI — OCR One-Liner
# Bearer Token ERFORDERLICH
# ═══════════════════════════════════════════════════════════════

set -euo pipefail

API_KEY="${PAPEROFFICE_API_KEY:?Bitte PAPEROFFICE_API_KEY setzen (export PAPEROFFICE_API_KEY=po_sk_xxx)}"
INPUT_FILE="${1:-document.png}"

if [ ! -f "$INPUT_FILE" ]; then
  echo "Verwendung: $0 <datei>"
  echo "Beispiel:   $0 document.png"
  exit 1
fi

echo "→ OCR für: $INPUT_FILE"

# ocr_mode: complete (+Tabellen), grid (+Bounding Boxes), text (nur Text)
curl -s -X POST "https://api.paperoffice.ai/latest/job/add/workflow" \
  -H "Authorization: Bearer ${API_KEY}" \
  -F "file_1=@${INPUT_FILE}" \
  -F "ocr_mode=complete" \
  -F "priority=900" | python3 -m json.tool
