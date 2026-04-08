#!/usr/bin/env bash
# PaperOffice AI — OCR Complete-Mode (Text + Bounding Boxes + Tabellen)

api_base="https://api.paperoffice.ai/latest"
api_key="${PAPEROFFICE_API_KEY:?Bitte PAPEROFFICE_API_KEY setzen}"
input_file="${1:?Bitte Dateipfad als Argument übergeben}"

response=$(curl -s "${api_base}/job/add/paperoffice_aiocr___generate" \
  -H "Authorization: Bearer ${api_key}" \
  -F "file_1=@${input_file}" \
  -F "ocr_mode=complete" \
  -F "priority=900")

# Zusammenfassung extrahieren
summary=$(echo "${response}" | python3 -c "
import sys, json
data = json.load(sys.stdin)
output = data.get('result', {}).get('output', {})
summary = output.get('summary', {})
pages = output.get('pages', {})
print(f'Seiten:  {summary.get(\"total_pages\")}')
print(f'Zeilen:  {summary.get(\"total_lines\")}')
print(f'Zeichen: {summary.get(\"total_chars\")}')
print()
for page_id, page_data in sorted(pages.items()):
    print(f'--- Seite {page_id} ---')
    print(f'  Konfidenz: {page_data.get(\"confidence_avg\")}')
    print(f'  Zeilen:    {page_data.get(\"line_count\")}')
    bbox = page_data.get('bounding_boxes')
    if bbox:
        print(f'  Bounding Boxes: {len(bbox)} Elemente')
    tables = page_data.get('tables')
    if tables:
        print(f'  Tabellen: {len(tables)} erkannt')
    print()
print('--- Volltext ---')
print(summary.get('poaiocr_extracted_fulltext', 'Kein Text extrahiert'))
")

echo "${summary}"
