#!/usr/bin/env bash
# PaperOffice AI — Query and visualize knowledge graph
set -euo pipefail

API_KEY="${PAPEROFFICE_API_KEY:?Please set PAPEROFFICE_API_KEY (export PAPEROFFICE_API_KEY=po_sk_xxx)}"
BASE_URL="https://api.paperoffice.ai/latest/knowledge_graph"
QUESTION="${1:-Who are the main business partners?}"
POFID="${2:-}"

echo "=== 1. Graph statistics ==="
curl -s -X GET "${BASE_URL}/stats" \
  -H "Authorization: Bearer ${API_KEY}" | python3 -m json.tool

echo ""
echo "=== 2. Query knowledge graph ==="
echo "Question: ${QUESTION}"

QUERY_ARGS=(-F "question=${QUESTION}" -F "max_hops=3")
if [ -n "${POFID}" ]; then
  QUERY_ARGS+=(-F "pofid=${POFID}")
  echo "Scoped to document: ${POFID}"
fi
echo ""

curl -s -X POST "${BASE_URL}/universe" \
  -H "Authorization: Bearer ${API_KEY}" \
  "${QUERY_ARGS[@]}" | python3 -m json.tool

echo ""
echo "=== 3. Get Mermaid visualization ==="

MERMAID_ARGS=(-F "format=mermaid")
if [ -n "${POFID}" ]; then
  MERMAID_ARGS+=(-F "pofid=${POFID}")
fi

curl -s -X POST "${BASE_URL}/universe" \
  -H "Authorization: Bearer ${API_KEY}" \
  "${MERMAID_ARGS[@]}" | python3 -m json.tool

echo ""
echo "=== 4. Business partners ==="
curl -s -X GET "${BASE_URL}/partners" \
  -H "Authorization: Bearer ${API_KEY}" | python3 -m json.tool
