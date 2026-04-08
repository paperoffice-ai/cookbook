#!/usr/bin/env bash
# PaperOffice AI — Create & list workspaces
set -euo pipefail

api_base="https://api.paperoffice.ai/latest"
api_key="${PAPEROFFICE_API_KEY:?Please set PAPEROFFICE_API_KEY}"

workspace_name="${1:-My Workspace}"
workspace_desc="${2:-Automatically created workspace}"

echo "→ Creating workspace: ${workspace_name}"

create_response=$(curl -s -X POST "${api_base}/documents/workspace-create" \
  -H "Authorization: Bearer ${api_key}" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "name=${workspace_name}" \
  -d "description=${workspace_desc}")

echo "${create_response}" | python3 -c "
import sys, json
data = json.load(sys.stdin)
if data.get('status') != 'success':
    print('Error:', json.dumps(data, indent=2))
    sys.exit(1)
ws = data.get('workspace', {})
print(f'  ID:          {ws.get(\"id\", \"—\")}')
print(f'  Name:        {ws.get(\"name\", \"—\")}')
print(f'  Description: {ws.get(\"description\", \"—\")}')
print(f'  Created:     {ws.get(\"created_at\", \"—\")}')
"

echo ""
echo "→ Listing all workspaces"

list_response=$(curl -s -X GET "${api_base}/documents/workspaces-list" \
  -H "Authorization: Bearer ${api_key}")

echo "${list_response}" | python3 -c "
import sys, json
data = json.load(sys.stdin)
if data.get('status') != 'success':
    print('Error:', json.dumps(data, indent=2))
    sys.exit(1)
workspaces = data.get('workspaces', [])
print(f'Found: {len(workspaces)} workspace(s)')
print()
for ws in workspaces:
    print(f'  [{ws.get(\"id\", \"—\")}] {ws.get(\"name\", \"—\")} — {ws.get(\"description\", \"\")}')
"
