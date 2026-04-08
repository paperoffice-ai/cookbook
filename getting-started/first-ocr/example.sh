#!/usr/bin/env bash
# PaperOffice AI — First OCR Call (Text Extraction)

api_base="https://api.paperoffice.ai/latest"
api_key="${PAPEROFFICE_API_KEY:?Please set PAPEROFFICE_API_KEY}"
input_file="${1:?Error: Please provide file path as argument}"

response=$(curl -s "${api_base}/job/add/paperoffice_aiocr___generate" \
  -H "Authorization: Bearer ${api_key}" \
  -F "file_1=@${input_file}" \
  -F "ocr_mode=text" \
  -F "priority=900")

# Show full response
echo "${response}" | python3 -m json.tool

# Print extracted text
fulltext=$(echo "${response}" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(data.get('result', {}).get('output', {}).get('summary', {}).get('poaiocr_extracted_fulltext', 'No text extracted'))
")
echo ""
echo "--- Extracted Text ---"
echo "${fulltext}"
