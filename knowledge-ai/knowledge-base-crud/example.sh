#!/usr/bin/env bash
# PaperOffice AI — Knowledge Base CRUD Operations
set -euo pipefail

API_KEY="${PAPEROFFICE_API_KEY:?Please set PAPEROFFICE_API_KEY (export PAPEROFFICE_API_KEY=po_sk_xxx)}"
BASE_URL="https://api.paperoffice.ai/latest/knowledge"

# Helper function for API calls
api_get() {
  curl -s -X GET "${BASE_URL}/$1" \
    -H "Authorization: Bearer ${API_KEY}"
}

api_post() {
  local endpoint="$1"; shift
  curl -s -X POST "${BASE_URL}/${endpoint}" \
    -H "Authorization: Bearer ${API_KEY}" \
    "$@"
}

echo "=== 1. List existing knowledge bases ==="
api_get "kb_list" | python3 -m json.tool

echo ""
echo "=== 2. Create new knowledge base ==="
CREATE_RESPONSE=$(api_post "kb_add" \
  -F "name=Cookbook-Test-KB" \
  -F "description=Test data for cookbook example" \
  -F "primary_language=de")

echo "${CREATE_RESPONSE}" | python3 -m json.tool

KB_ID=$(echo "${CREATE_RESPONSE}" | python3 -c "
import sys,json
d=json.load(sys.stdin)
# Support different response formats
kb_id = ''
if 'data' in d and isinstance(d['data'], dict):
    kb_id = str(d['data'].get('id', ''))
if not kb_id:
    kb_id = str(d.get('kb_id', d.get('id', '')))
print(kb_id)
" 2>/dev/null || echo "")

if [ -z "${KB_ID}" ]; then
  echo "⚠ KB created, but no KB ID in response. Skipping article operations."
  echo ""
  echo "=== Fallback: Show existing KBs ==="
  api_get "kb_list" | python3 -c "
import sys,json
d=json.load(sys.stdin)
for kb in d.get('data',[]):
    print(f\"  [{kb['id']}] {kb['name']} ({kb['status']})\")
"
  exit 0
fi
echo "→ KB ID: ${KB_ID}"

echo ""
echo "=== 3. Add articles to KB ==="
api_post "add" \
  -F "kb_id=${KB_ID}" \
  -F "title=Getting Started with PaperOffice" \
  -F "content=PaperOffice AI provides intelligent document processing, OCR and knowledge management." \
  -F "category=Introduction" | python3 -m json.tool

api_post "add" \
  -F "kb_id=${KB_ID}" \
  -F "title=API Authentication" \
  -F "content=All API calls require a Bearer Token in the Authorization header." \
  -F "category=Technical" | python3 -m json.tool

echo ""
echo "=== 4. List articles ==="
api_get "list?kb_id=${KB_ID}" | python3 -m json.tool

echo ""
echo "=== 5. Cleanup — Delete KB ==="
api_post "kb_delete" -F "id=${KB_ID}" | python3 -m json.tool

echo ""
echo "✓ CRUD cycle completed."
