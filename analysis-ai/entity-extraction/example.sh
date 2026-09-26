#!/usr/bin/env bash
# PaperOffice AI — Entities of a processed document
set -euo pipefail

API_KEY="${PAPEROFFICE_API_KEY:?Please set PAPEROFFICE_API_KEY (export PAPEROFFICE_API_KEY=po_ut_xxx)}"
DOCUMENTS_ID="${1:?Usage: $0 <documents_id> [type]  — find documents_id with POST /documents/document-search}"
TYPE="${2:-}"

echo "→ Entities of document ${DOCUMENTS_ID}${TYPE:+ (type: $TYPE)}"

curl -s -G "https://api.paperoffice.ai/latest/document_intelligence/entities" \
  -H "Authorization: Bearer ${API_KEY}" \
  --data-urlencode "documents_id=${DOCUMENTS_ID}" \
  ${TYPE:+--data-urlencode "type=${TYPE}"} | python3 -m json.tool
