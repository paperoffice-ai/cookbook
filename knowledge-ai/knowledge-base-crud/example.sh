#!/usr/bin/env bash
# PaperOffice AI — Knowledge Base CRUD-Operationen
set -euo pipefail

API_KEY="${PAPEROFFICE_API_KEY:?Bitte PAPEROFFICE_API_KEY setzen (export PAPEROFFICE_API_KEY=po_sk_xxx)}"
BASE_URL="https://api.paperoffice.ai/latest/knowledge"

# Hilfsfunktion für API-Aufrufe
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

echo "=== 1. Bestehende Knowledge Bases auflisten ==="
api_get "kb_list" | python3 -m json.tool

echo ""
echo "=== 2. Neue Knowledge Base erstellen ==="
CREATE_RESPONSE=$(api_post "kb_create" \
  -F "name=Cookbook-Test-KB" \
  -F "description=Testdaten für Cookbook-Beispiel" \
  -F "primary_language=de")

echo "${CREATE_RESPONSE}" | python3 -m json.tool

KB_ID=$(echo "${CREATE_RESPONSE}" | python3 -c "
import sys,json
d=json.load(sys.stdin)
# Verschiedene Antwortformate unterstützen
kb_id = ''
if 'data' in d and isinstance(d['data'], dict):
    kb_id = str(d['data'].get('id', ''))
if not kb_id:
    kb_id = str(d.get('kb_id', d.get('id', '')))
print(kb_id)
" 2>/dev/null || echo "")

if [ -z "${KB_ID}" ]; then
  echo "⚠ KB erstellt, aber keine KB-ID in Antwort. Überspringe Artikel-Operationen."
  echo ""
  echo "=== Fallback: Bestehende KBs anzeigen ==="
  api_get "kb_list" | python3 -c "
import sys,json
d=json.load(sys.stdin)
for kb in d.get('data',[]):
    print(f\"  [{kb['id']}] {kb['name']} ({kb['status']})\")
"
  exit 0
fi
echo "→ KB-ID: ${KB_ID}"

echo ""
echo "=== 3. Artikel zur KB hinzufügen ==="
api_post "article_create" \
  -F "kb_id=${KB_ID}" \
  -F "title=Erste Schritte mit PaperOffice" \
  -F "content=PaperOffice AI bietet intelligente Dokumentenverarbeitung, OCR und Knowledge Management." \
  -F "category=Einführung" | python3 -m json.tool

api_post "article_create" \
  -F "kb_id=${KB_ID}" \
  -F "title=API-Authentifizierung" \
  -F "content=Alle API-Aufrufe benötigen einen Bearer Token im Authorization-Header." \
  -F "category=Technik" | python3 -m json.tool

echo ""
echo "=== 4. Artikel auflisten ==="
api_get "article_list?kb_id=${KB_ID}" | python3 -m json.tool

echo ""
echo "=== 5. Aufräumen — KB löschen ==="
api_post "kb_delete" -F "kb_id=${KB_ID}" | python3 -m json.tool

echo ""
echo "✓ CRUD-Zyklus abgeschlossen."
