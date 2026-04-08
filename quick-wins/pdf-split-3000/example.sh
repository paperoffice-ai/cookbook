#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════
# PaperOffice AI — AI PDF Split (bis 3000 Seiten)
# Bearer Token ERFORDERLICH
# ═══════════════════════════════════════════════════════════════

set -euo pipefail

API_KEY="${PAPEROFFICE_API_KEY:?Bitte PAPEROFFICE_API_KEY setzen (export PAPEROFFICE_API_KEY=po_sk_xxx)}"
INPUT_FILE="${1:-sammel_dokument.pdf}"

if [ ! -f "$INPUT_FILE" ]; then
  echo "Verwendung: $0 <pdf-datei>"
  echo "Beispiel:   $0 sammel_dokument.pdf"
  exit 1
fi

echo "→ AI PDF Split für: $INPUT_FILE"

curl -s -X POST "https://api.paperoffice.ai/latest/job" \
  -H "Authorization: Bearer ${API_KEY}" \
  -F "file=@${INPUT_FILE}" \
  -F "template=pdf_ai_split" \
  -F "naming_instruction=Dokumenttyp_Datum_Absender" \
  -F "locale=de_DE" \
  -F "priority=900" | python3 -m json.tool
