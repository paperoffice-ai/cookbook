#!/usr/bin/env bash
# PaperOffice AI — Entity-Extraktion (NER) aus Text
set -euo pipefail

API_KEY="${PAPEROFFICE_API_KEY:?Bitte PAPEROFFICE_API_KEY setzen (export PAPEROFFICE_API_KEY=po_sk_xxx)}"
TEXT="${1:-Die Mustermann GmbH mit Sitz in München hat am 15. März 2025 einen Vertrag über 250.000 EUR mit der Beispiel AG abgeschlossen.}"

echo "→ Entity-Extraktion für Text:"
echo "  \"${TEXT:0:80}...\""
echo ""

curl -s -X POST "https://api.paperoffice.ai/latest/document_intelligence/entities" \
  -H "Authorization: Bearer ${API_KEY}" \
  -F "text=${TEXT}" | python3 -m json.tool
