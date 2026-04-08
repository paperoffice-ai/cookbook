#!/usr/bin/env bash
# PaperOffice AI — Knowledge Base semantische Suche
set -euo pipefail

API_KEY="${PAPEROFFICE_API_KEY:?Bitte PAPEROFFICE_API_KEY setzen (export PAPEROFFICE_API_KEY=po_sk_xxx)}"
QUERY="${1:-Wie funktioniert die API-Authentifizierung?}"
KB_ID="${2:-}"
LIMIT="${3:-5}"

echo "=== Knowledge Base Suche ==="
echo "Frage: ${QUERY}"
[ -n "${KB_ID}" ] && echo "KB-ID: ${KB_ID}"
echo "Limit: ${LIMIT}"
echo ""

ARGS=(-F "query=${QUERY}" -F "limit=${LIMIT}")
[ -n "${KB_ID}" ] && ARGS+=(-F "kb_id=${KB_ID}")

curl -s -X POST "https://api.paperoffice.ai/latest/knowledge/search" \
  -H "Authorization: Bearer ${API_KEY}" \
  "${ARGS[@]}" | python3 -m json.tool
