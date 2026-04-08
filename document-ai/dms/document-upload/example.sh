#!/usr/bin/env bash
# PaperOffice AI — Dokument ins DMS hochladen
set -euo pipefail

api_base="https://api.paperoffice.ai/latest"
api_key="${PAPEROFFICE_API_KEY:?Bitte PAPEROFFICE_API_KEY setzen}"

input_file="${1:?Bitte Dateipfad als Argument übergeben}"
workspace="${2:?Bitte Workspace-Name als zweites Argument übergeben}"
tags="${3:-}"

if [ ! -f "${input_file}" ]; then
  echo "Datei nicht gefunden: ${input_file}"
  exit 1
fi

echo "→ Lade hoch: ${input_file} → Workspace: ${workspace}"

curl_args=(
  -s -X POST "${api_base}/documents/upload"
  -H "Authorization: Bearer ${api_key}"
  -F "file_1=@${input_file}"
  -F "workspace_name=${workspace}"
)

if [ -n "${tags}" ]; then
  curl_args+=(-F "tags=${tags}")
fi

response=$(curl "${curl_args[@]}")

echo "${response}" | python3 -c "
import sys, json
data = json.load(sys.stdin)
if data.get('status') != 'success':
    print('Fehler:', json.dumps(data, indent=2))
    sys.exit(1)
doc = data.get('document', {})
print(f'  ID:        {doc.get(\"id\", \"—\")}')
print(f'  Dateiname: {doc.get(\"filename\", \"—\")}')
print(f'  Workspace: {doc.get(\"workspace\", \"—\")}')
print(f'  Tags:      {doc.get(\"tags\", [])}')
print(f'  Größe:     {doc.get(\"size\", \"—\")}')
print(f'  Erstellt:  {doc.get(\"created_at\", \"—\")}')
"
