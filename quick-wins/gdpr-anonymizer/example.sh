#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════
# PaperOffice AI — DSGVO Anonymisierung (PII Preview)
# Bearer Token ERFORDERLICH
# ═══════════════════════════════════════════════════════════════

set -euo pipefail

API_KEY="${PAPEROFFICE_API_KEY:?Bitte PAPEROFFICE_API_KEY setzen (export PAPEROFFICE_API_KEY=po_sk_xxx)}"
INPUT_FILE="${1:-dokument.pdf}"

if [ ! -f "$INPUT_FILE" ]; then
  echo "Verwendung: $0 <datei>"
  echo "Beispiel:   $0 dokument.pdf"
  exit 1
fi

echo "→ DSGVO Anonymisierung (Preview) für: $INPUT_FILE"

curl -s -X POST "https://api.paperoffice.ai/latest/job/add/workflow" \
  -H "Authorization: Bearer ${API_KEY}" \
  -F "file=@${INPUT_FILE}" \
  -F "template=document_anonymize_preview" \
  -F "redact_categories=all" \
  -F "priority=900" | python3 -m json.tool
