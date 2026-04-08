#!/usr/bin/env bash
# PaperOffice AI — AI-powered document generation
set -euo pipefail

api_base="https://api.paperoffice.ai/latest"
api_key="${PAPEROFFICE_API_KEY:?Please set PAPEROFFICE_API_KEY}"

template="${1:?Please provide template name as argument}"
output_format="${2:-pdf}"

# Example variables for an invoice
variables='{"firma":"Muster GmbH","rechnungsnummer":"2026-042","betrag":"1.250,00","datum":"08.04.2026"}'

echo "→ Generating document from template: ${template} (${output_format})"

response=$(curl -s -X POST "${api_base}/document_generation/generate" \
  -H "Authorization: Bearer ${api_key}" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "template=${template}" \
  -d "variables=${variables}" \
  -d "output_format=${output_format}")

echo "${response}" | python3 -c "
import sys, json
data = json.load(sys.stdin)
if data.get('status') != 'success':
    print('Error:', json.dumps(data, indent=2))
    sys.exit(1)
doc = data.get('document', {})
print(f'  Download URL: {doc.get(\"download_url\", \"—\")}')
print(f'  Format:       {doc.get(\"format\", \"—\")}')
print(f'  Pages:        {doc.get(\"pages\", \"—\")}')
"
