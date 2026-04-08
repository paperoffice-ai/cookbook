#!/usr/bin/env bash
# PaperOffice AI — Chat with a document (RAG)
set -euo pipefail

api_base="https://api.paperoffice.ai/latest"
api_key="${PAPEROFFICE_API_KEY:?Please set PAPEROFFICE_API_KEY}"

document_id="${1:?Please provide document ID as argument}"
question="${2:?Please provide question as second argument}"

echo "→ Question to document ${document_id}: ${question}"

response=$(curl -s -X POST "${api_base}/document_intelligence/chat" \
  -H "Authorization: Bearer ${api_key}" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "document_id=${document_id}" \
  -d "question=${question}")

echo "${response}" | python3 -c "
import sys, json
data = json.load(sys.stdin)
if data.get('status') != 'success':
    print('Error:', json.dumps(data, indent=2))
    sys.exit(1)

print()
print('Answer:')
print(data.get('answer', '—'))
print()

sources = data.get('sources', [])
if sources:
    print(f'Sources ({len(sources)}):')
    for s in sources:
        page = s.get('page', '—')
        conf = s.get('confidence', '—')
        text = s.get('text', '')[:100]
        print(f'  Page {page} [{conf}]: {text}')
"
