#!/usr/bin/env bash
# PaperOffice AI — Knowledge Graph aufbauen und abfragen
set -euo pipefail

API_KEY="${PAPEROFFICE_API_KEY:?Bitte PAPEROFFICE_API_KEY setzen (export PAPEROFFICE_API_KEY=po_sk_xxx)}"
BASE_URL="https://api.paperoffice.ai/latest/knowledge_graph"
TEXT="${1:-Die Mustermann GmbH hat ihren Hauptsitz in München. CEO ist Max Mustermann. Das Unternehmen wurde 2010 gegründet und beschäftigt 500 Mitarbeiter. Hauptkunde ist die Beispiel AG aus Berlin.}"

echo "=== 1. Knowledge Graph aufbauen ==="
echo "Text: ${TEXT:0:80}..."
echo ""

BUILD_RESPONSE=$(curl -s -X POST "${BASE_URL}/build" \
  -H "Authorization: Bearer ${API_KEY}" \
  -F "text=${TEXT}")

echo "${BUILD_RESPONSE}" | python3 -m json.tool

GRAPH_ID=$(echo "${BUILD_RESPONSE}" | python3 -c "import sys,json; print(json.load(sys.stdin).get('graph_id',''))" 2>/dev/null || echo "")

if [ -z "${GRAPH_ID}" ]; then
  echo "⚠ Kein graph_id erhalten, Query übersprungen."
  exit 0
fi

echo ""
echo "=== 2. Knowledge Graph abfragen ==="
echo "Graph-ID: ${GRAPH_ID}"
echo "Frage: Wer ist der CEO der Mustermann GmbH?"
echo ""

curl -s -X POST "${BASE_URL}/query" \
  -H "Authorization: Bearer ${API_KEY}" \
  -F "graph_id=${GRAPH_ID}" \
  -F "query=Wer ist der CEO der Mustermann GmbH?" | python3 -m json.tool
