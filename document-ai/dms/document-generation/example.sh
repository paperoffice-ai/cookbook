#!/usr/bin/env bash
# PaperOffice AI — KI-basierte Dokumentenerstellung
set -euo pipefail

api_base="https://api.paperoffice.ai/latest"
api_key="${PAPEROFFICE_API_KEY:?Bitte PAPEROFFICE_API_KEY setzen}"

template="${1:?Bitte Template-Name als Argument übergeben}"
output_format="${2:-pdf}"

# Beispiel-Variablen für eine Rechnung
variables='{"firma":"Muster GmbH","rechnungsnummer":"2026-042","betrag":"1.250,00","datum":"08.04.2026"}'

echo "→ Generiere Dokument aus Template: ${template} (${output_format})"

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
    print('Fehler:', json.dumps(data, indent=2))
    sys.exit(1)
doc = data.get('document', {})
print(f'  Download-URL: {doc.get(\"download_url\", \"—\")}')
print(f'  Format:       {doc.get(\"format\", \"—\")}')
print(f'  Seiten:       {doc.get(\"pages\", \"—\")}')
"
