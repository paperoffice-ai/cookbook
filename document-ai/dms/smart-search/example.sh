#!/usr/bin/env bash
# PaperOffice AI — Smart document search in DMS
set -euo pipefail

api_base="https://api.paperoffice.ai/latest"
api_key="${PAPEROFFICE_API_KEY:?Please set PAPEROFFICE_API_KEY}"

search_term="${1:?Please provide search term as argument}"
workspace_id="${2:?Please provide workspace_id as second argument}"
limit="${3:-20}"

echo "→ Searching for: ${search_term} (workspace ${workspace_id})"

response=$(curl -s -X POST "${api_base}/documents/documents-list" \
  -H "Authorization: Bearer ${api_key}" \
  -H "Content-Type: application/json" \
  -d "{
    \"workspace_id\": ${workspace_id},
    \"global_search\": \"${search_term}\",
    \"search_mode\": \"intelligent\",
    \"search_preference\": \"balanced\",
    \"limit\": ${limit}
  }")

echo "${response}" | python3 -c "
import sys, json
data = json.load(sys.stdin)
if data.get('status') != 'success':
    print('Error:', json.dumps(data, indent=2))
    sys.exit(1)
results = data.get('results', data.get('data', []))
total = data.get('total', len(results))
print(f'Hits: {total}')
print()
for r in results:
    score = r.get('score', '—')
    print(f'  [{r.get(\"id\", \"—\")}] {r.get(\"filename\", r.get(\"file_name\", \"—\"))} (Score: {score})')
    snippet = r.get('snippet', '')
    if snippet:
        print(f'        {snippet[:120]}')
    print()
"
