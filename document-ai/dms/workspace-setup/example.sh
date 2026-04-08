#!/usr/bin/env bash
# PaperOffice AI — Workspace erstellen & auflisten
set -euo pipefail

api_base="https://api.paperoffice.ai/latest"
api_key="${PAPEROFFICE_API_KEY:?Bitte PAPEROFFICE_API_KEY setzen}"

workspace_name="${1:-Mein Workspace}"
workspace_desc="${2:-Automatisch erstellter Workspace}"

echo "→ Erstelle Workspace: ${workspace_name}"

create_response=$(curl -s -X POST "${api_base}/documents/workspace_create" \
  -H "Authorization: Bearer ${api_key}" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "name=${workspace_name}" \
  -d "description=${workspace_desc}")

echo "${create_response}" | python3 -c "
import sys, json
data = json.load(sys.stdin)
if data.get('status') != 'success':
    print('Fehler:', json.dumps(data, indent=2))
    sys.exit(1)
ws = data.get('workspace', {})
print(f'  ID:          {ws.get(\"id\", \"—\")}')
print(f'  Name:        {ws.get(\"name\", \"—\")}')
print(f'  Beschreibung:{ws.get(\"description\", \"—\")}')
print(f'  Erstellt:    {ws.get(\"created_at\", \"—\")}')
"

echo ""
echo "→ Alle Workspaces auflisten"

list_response=$(curl -s -X GET "${api_base}/documents/workspace_list" \
  -H "Authorization: Bearer ${api_key}")

echo "${list_response}" | python3 -c "
import sys, json
data = json.load(sys.stdin)
if data.get('status') != 'success':
    print('Fehler:', json.dumps(data, indent=2))
    sys.exit(1)
workspaces = data.get('workspaces', [])
print(f'Gefunden: {len(workspaces)} Workspace(s)')
print()
for ws in workspaces:
    print(f'  [{ws.get(\"id\", \"—\")}] {ws.get(\"name\", \"—\")} — {ws.get(\"description\", \"\")}')
"
