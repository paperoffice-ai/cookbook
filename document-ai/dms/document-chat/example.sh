#!/usr/bin/env bash
# PaperOffice AI — Chat mit einem Dokument (RAG)
set -euo pipefail

api_base="https://api.paperoffice.ai/latest"
api_key="${PAPEROFFICE_API_KEY:?Bitte PAPEROFFICE_API_KEY setzen}"

document_id="${1:?Bitte Document-ID als Argument übergeben}"
question="${2:?Bitte Frage als zweites Argument übergeben}"

echo "→ Frage an Dokument ${document_id}: ${question}"

response=$(curl -s -X POST "${api_base}/document_intelligence/chat" \
  -H "Authorization: Bearer ${api_key}" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "document_id=${document_id}" \
  -d "question=${question}")

echo "${response}" | python3 -c "
import sys, json
data = json.load(sys.stdin)
if data.get('status') != 'success':
    print('Fehler:', json.dumps(data, indent=2))
    sys.exit(1)

print()
print('Antwort:')
print(data.get('answer', '—'))
print()

sources = data.get('sources', [])
if sources:
    print(f'Quellen ({len(sources)}):')
    for s in sources:
        page = s.get('page', '—')
        conf = s.get('confidence', '—')
        text = s.get('text', '')[:100]
        print(f'  Seite {page} [{conf}]: {text}')
"
