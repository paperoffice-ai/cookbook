#!/usr/bin/env bash
# PaperOffice AI — Chat with documents via GraphRAG
set -euo pipefail

api_key="${PAPEROFFICE_API_KEY:?Please set PAPEROFFICE_API_KEY (export PAPEROFFICE_API_KEY=po_sk_xxx)}"
api_base="https://api.paperoffice.ai/latest"
question="${1:?Usage: $0 <question> [pofid]}"
pofid="${2:-}"

echo "Question: ${question}"

args=(-F "question=${question}" -F "max_hops=3")
if [ -n "${pofid}" ]; then
  args+=(-F "pofid=${pofid}")
  echo "Document: ${pofid}"
fi
echo ""

response=$(curl -s -X POST "${api_base}/knowledge_graph/universe" \
  -H "Authorization: Bearer ${api_key}" \
  "${args[@]}")

echo "${response}" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print('Answer:', data.get('answer', '(no answer)'))
conf = data.get('confidence')
if conf:
    print(f'Confidence: {conf}')
nodes = data.get('relevant_nodes', [])
if nodes:
    print(f'Evidence ({len(nodes)} nodes):')
    for n in nodes[:5]:
        print(f'  - {n.get(\"label\", n.get(\"id\", \"?\"))} ({n.get(\"type\", \"?\")})')
"
