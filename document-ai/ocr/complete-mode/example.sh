#!/usr/bin/env bash
# PaperOffice AI — OCR Complete-Mode (text + bounding boxes + tables)

api_base="https://api.paperoffice.ai/latest"
api_key="${PAPEROFFICE_API_KEY:?Please set PAPEROFFICE_API_KEY}"
input_file="${1:?Please provide file path as argument}"

response=$(curl -s "${api_base}/job/add/paperoffice_aiocr___generate" \
  -H "Authorization: Bearer ${api_key}" \
  -F "file_1=@${input_file}" \
  -F "ocr_mode=complete" \
  -F "priority=900")

# Extract summary
summary=$(echo "${response}" | python3 -c "
import sys, json
data = json.load(sys.stdin)
output = data.get('result', {}).get('output', {})
summary = output.get('summary', {})
pages = output.get('pages', {})
print(f'Pages:      {summary.get(\"total_pages\")}')
print(f'Lines:      {summary.get(\"total_lines\")}')
print(f'Characters: {summary.get(\"total_chars\")}')
print()
for page_id, page_data in sorted(pages.items()):
    print(f'--- Page {page_id} ---')
    print(f'  Confidence: {page_data.get(\"confidence_avg\")}')
    print(f'  Lines:      {page_data.get(\"line_count\")}')
    bbox = page_data.get('bounding_boxes')
    if bbox:
        print(f'  Bounding Boxes: {len(bbox)} elements')
    tables = page_data.get('tables')
    if tables:
        print(f'  Tables: {len(tables)} detected')
    print()
print('--- Full text ---')
print(summary.get('poaiocr_extracted_fulltext', 'No text extracted'))
")

echo "${summary}"
