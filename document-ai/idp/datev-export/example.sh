#!/usr/bin/env bash
# PaperOffice AI — DATEV Export from Invoice IDP
set -euo pipefail

api_base="https://api.paperoffice.ai/latest"
api_key="${PAPEROFFICE_API_KEY:?Please set PAPEROFFICE_API_KEY}"
input_file="${1:?Please provide file path as argument}"

if [ ! -f "${input_file}" ]; then
  echo "File not found: ${input_file}"
  exit 1
fi

echo "→ Extracting invoice and converting to DATEV: ${input_file}"

response=$(curl -s -X POST "${api_base}/job/add/workflow" \
  -H "Authorization: Bearer ${api_key}" \
  -F "file_1=@${input_file}" \
  -F "model=premium" \
  -F "idp_collection=invoice" \
  -F "priority=900")

# Convert IDP result to DATEV accounting entry
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

def get_field(name):
    info = fields.get(name, {})
    return info.get('value_raw', info.get('value', ''))

# DATEV accounting entry fields
umsatz = get_field('_total_amount')
datum = get_field('_invoice_date')
re_nr = get_field('_invoice_number')
lieferant = get_field('_supplier_name')

# Date format DDMM for DATEV
datev_datum = ''
if datum and len(datum) >= 10:
    teile = datum.split('-')
    if len(teile) == 3:
        datev_datum = f'{teile[2]}{teile[1]}'

# CSV header (DATEV posting batch mandatory fields)
header = 'Umsatz (ohne Soll/Haben-Kz);Soll/Haben-Kennzeichen;Konto;Gegenkonto;BU-Schlüssel;Belegdatum;Belegfeld 1;Buchungstext'
zeile = f'{umsatz};S;70000;1200;;{datev_datum};{re_nr};{lieferant}'

print('--- DATEV Accounting Entry (CSV) ---')
print(header)
print(zeile)
"
