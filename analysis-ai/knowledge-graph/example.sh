#!/usr/bin/env bash
# PaperOffice AI — Knowledge Graph: statistics, question, business partners
set -euo pipefail

API_KEY="${PAPEROFFICE_API_KEY:?Please set PAPEROFFICE_API_KEY (export PAPEROFFICE_API_KEY=po_ut_xxx)}"
WORKSPACE_ID="${1:?Usage: $0 <workspace_id> [question]}"
QUESTION="${2:-Who are the main business partners?}"
BASE="https://api.paperoffice.ai/latest/knowledge_graph"

echo "=== Graph statistics ==="
curl -s -G "${BASE}/stats" -H "Authorization: Bearer ${API_KEY}" --data-urlencode "workspace_id=${WORKSPACE_ID}" | python3 -m json.tool | head -40

echo; echo "=== Question: ${QUESTION} ==="
curl -s -m 180 -X POST "${BASE}/ask" -H "Authorization: Bearer ${API_KEY}" -H "Content-Type: application/json" \
  -d "$(python3 -c 'import json,sys;print(json.dumps({"question":sys.argv[1],"workspace_id":int(sys.argv[2])}))' "${QUESTION}" "${WORKSPACE_ID}")" \
  | python3 -c 'import sys,json;d=json.load(sys.stdin);print("Answer: ",d.get("answer",""));print("Routing:",d.get("routing"));[print("  source:",s.get("file_name")) for s in d.get("sources",[])[:5]]'

echo; echo "=== Business partners ==="
curl -s -G "${BASE}/partners" -H "Authorization: Bearer ${API_KEY}" --data-urlencode "workspace_id=${WORKSPACE_ID}" \
  | python3 -c 'import sys,json;[print("  -",p.get("name"),":",p.get("document_count"),"documents") for p in json.load(sys.stdin).get("partners",[])[:10]]'
