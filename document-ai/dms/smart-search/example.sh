#!/usr/bin/env bash
# PaperOffice AI — Intelligente Dokumentensuche im DMS
set -euo pipefail

api_base="https://api.paperoffice.ai/latest"
api_key="${PAPEROFFICE_API_KEY:?Bitte PAPEROFFICE_API_KEY setzen}"

search_term="${1:?Bitte Suchbegriff als Argument übergeben}"
workspace="${2:-}"
limit="${3:-10}"

echo "→ Suche nach: ${search_term}"

curl_args=(
  -s -X POST "${api_base}/documents/search"
  -H "Authorization: Bearer ${api_key}"
  -H "Content-Type: application/x-www-form-urlencoded"
  -d "global_search=${search_term}"
  -d "limit=${limit}"
)

if [ -n "${workspace}" ]; then
  curl_args+=(-d "workspace_name=${workspace}")
fi

response=$(curl "${curl_args[@]}")

echo "${response}" | python3 -c "
import sys, json
data = json.load(sys.stdin)
if data.get('status') != 'success':
    print('Fehler:', json.dumps(data, indent=2))
    sys.exit(1)
results = data.get('results', [])
total = data.get('total', len(results))
print(f'Treffer: {total}')
print()
for r in results:
    score = r.get('score', '—')
    print(f'  [{r.get(\"id\", \"—\")}] {r.get(\"filename\", \"—\")} (Score: {score})')
    print(f'        Workspace: {r.get(\"workspace\", \"—\")}')
    snippet = r.get('snippet', '')
    if snippet:
        print(f'        {snippet[:120]}')
    print()
"
