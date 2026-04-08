#!/usr/bin/env bash
# PaperOffice AI — IDP with Custom Extraction Fields (Custom Fields)
set -euo pipefail

api_base="https://api.paperoffice.ai/latest"
api_key="${PAPEROFFICE_API_KEY:?Please set PAPEROFFICE_API_KEY}"
input_file="${1:?Please provide file path as argument}"

if [ ! -f "${input_file}" ]; then
  echo "File not found: ${input_file}"
  exit 1
fi

# Define custom fields as JSON
idp_fields='[
  {"name":"vertragsnummer","type":"string","description":"Contract number in the document"},
  {"name":"kuendigungsfrist","type":"string","description":"Cancellation period in months or as a date"},
  {"name":"monatlicher_betrag","type":"number","description":"Monthly amount in euros"},
  {"name":"vertragspartner","type":"string","description":"Name of the contracting party"}
]'

echo "→ Extracting custom fields from: ${input_file}"

response=$(curl -s -X POST "${api_base}/job/add/workflow" \
  -H "Authorization: Bearer ${api_key}" \
  -F "file_1=@${input_file}" \
  -F "model=premium" \
  -F "idp_fields=${idp_fields}" \
  -F "priority=900")

echo "${response}" | python3 -c "
import sys, json

data = json.load(sys.stdin)
if data.get('status') != 'success':
    print('Error:', json.dumps(data, indent=2))
    sys.exit(1)

pages = data.get('result', {}).get('pages_idp', [])
if not pages:
    print('No IDP data found')
    sys.exit(1)

fields = pages[0].get('suggested_fields', {})
print(f'Job ID: {data.get(\"job_id\", \"—\")}')
print(f'Fields found: {len(fields)}')
print()
if isinstance(fields, dict):
    for name, info in sorted(fields.items()):
        val = str(info.get('value') or '—')
        conf = str(info.get('source_boxes_confidence') or '—')
        print(f'  {name:30s} {val:40s} [{conf}]')
elif isinstance(fields, list):
    for info in fields:
        name = str(info.get('name') or info.get('label') or '—')
        val = str(info.get('value') or '—')
        conf = str(info.get('source_boxes_confidence') or info.get('confidence') or '—')
        print(f'  {name:30s} {val:40s} [{conf}]')
"
