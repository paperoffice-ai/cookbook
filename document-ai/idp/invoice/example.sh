#!/usr/bin/env bash
# PaperOffice AI — Rechnungs-Extraktion (IDP Invoice)
set -euo pipefail

api_base="https://api.paperoffice.ai/latest"
api_key="${PAPEROFFICE_API_KEY:?Bitte PAPEROFFICE_API_KEY setzen}"
input_file="${1:?Bitte Dateipfad als Argument übergeben}"

if [ ! -f "${input_file}" ]; then
  echo "Datei nicht gefunden: ${input_file}"
  exit 1
fi

echo "→ Extrahiere Rechnungsdaten aus: ${input_file}"

response=$(curl -s -X POST "${api_base}/job/add/workflow" \
  -H "Authorization: Bearer ${api_key}" \
  -F "file_1=@${input_file}" \
  -F "model=premium" \
  -F "idp_collection=invoice" \
  -F "priority=900")

echo "${response}" | python3 -c "
import sys, json

data = json.load(sys.stdin)
if data.get('status') != 'success':
    print('Fehler:', json.dumps(data, indent=2))
    sys.exit(1)

pages = data.get('result', {}).get('pages_idp', [])
if not pages:
    print('Keine IDP-Daten gefunden')
    sys.exit(1)

fields = pages[0].get('suggested_fields', {})
print(f'Job-ID: {data.get(\"job_id\", \"—\")}')
print(f'Felder gefunden: {len(fields)}')
print()
for name, info in sorted(fields.items()):
    if info.get('type') == 'table':
        continue
    val = str(info.get('value') or '—')
    conf = str(info.get('source_boxes_confidence') or '—')
    print(f'  {name:30s} {val:40s} [{conf}]')
"
