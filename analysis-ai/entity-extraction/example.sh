#!/usr/bin/env bash
# PaperOffice AI — Entity extraction (NER) from text
set -euo pipefail

API_KEY="${PAPEROFFICE_API_KEY:?Please set PAPEROFFICE_API_KEY (export PAPEROFFICE_API_KEY=po_sk_xxx)}"
TEXT="${1:-Acme Corporation, based in New York, signed a contract worth 250,000 USD with Example Inc. on March 15, 2025. Contact: John Smith, +1 212 555 0123.}"

echo "→ Entity extraction for text:"
echo "  \"${TEXT:0:80}...\""
echo ""

curl -s -X POST "https://api.paperoffice.ai/latest/document_intelligence/entities" \
  -H "Authorization: Bearer ${API_KEY}" \
  -F "text=${TEXT}" | python3 -m json.tool
