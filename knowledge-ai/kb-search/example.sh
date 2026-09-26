#!/usr/bin/env bash
# PaperOffice AI — Knowledge Base semantic search
set -euo pipefail

API_KEY="${PAPEROFFICE_API_KEY:?Please set PAPEROFFICE_API_KEY (export PAPEROFFICE_API_KEY=po_ut_xxx)}"
QUERY="${1:-How does API authentication work?}"
KB_ID="${2:-}"
LIMIT="${3:-5}"

echo "=== Knowledge Base Search ==="
echo "Query: ${QUERY}"
[ -n "${KB_ID}" ] && echo "KB ID: ${KB_ID}"
echo "Limit: ${LIMIT}"
echo ""

ARGS=(-F "query=${QUERY}" -F "limit=${LIMIT}")
[ -n "${KB_ID}" ] && ARGS+=(-F "kb_id=${KB_ID}")

curl -s -X POST "https://api.paperoffice.ai/latest/knowledge/search" \
  -H "Authorization: Bearer ${API_KEY}" \
  "${ARGS[@]}" | python3 -m json.tool
