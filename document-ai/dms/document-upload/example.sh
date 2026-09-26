#!/usr/bin/env bash
# PaperOffice AI — Upload document to DMS
set -euo pipefail

api_base="https://api.paperoffice.ai/latest"
api_key="${PAPEROFFICE_API_KEY:?Please set PAPEROFFICE_API_KEY}"

input_file="${1:?Please provide file path as argument}"
workspace="${2:?Please provide workspace name as second argument}"
tags="${3:-}"

if [ ! -f "${input_file}" ]; then
  echo "File not found: ${input_file}"
  exit 1
fi

echo "→ Uploading: ${input_file} → Workspace: ${workspace}"

curl_args=(
  -s -X POST "${api_base}/documents/document-put"
  -H "Authorization: Bearer ${api_key}"
  -F "file=@${input_file}"
  -F "workspace_id=${workspace}"
)

if [ -n "${tags}" ]; then
  curl_args+=(-F "tags=${tags}")
fi

response=$(curl "${curl_args[@]}")

echo "${response}" | python3 -c "
import sys, json
data = json.load(sys.stdin)
if data.get('status') != 'success':
    print('Error:', json.dumps(data, indent=2))
    sys.exit(1)
for doc in data.get('results', []):
    print('  documents_id:', doc.get('documents_id', '-'))
    print('  POFID:       ', doc.get('pofid', '-'))
    print('  Filename:    ', doc.get('filename', '-'))
    print('  Workspace:   ', doc.get('workspace_name', '-'), '(id', doc.get('workspace_id', '-'), ')')
    print('  Size:        ', doc.get('size', '-'), 'bytes, pages:', doc.get('total_pages', '-'))
"
