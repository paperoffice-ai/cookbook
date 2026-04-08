#!/usr/bin/env bash
# PaperOffice AI — Generate searchable PDF (OCR + Searchable PDF)

api_base="https://api.paperoffice.ai/latest"
api_key="${PAPEROFFICE_API_KEY:?Please set PAPEROFFICE_API_KEY}"
input_file="${1:?Please provide file path as argument}"
output_file="${2:-searchable_output.pdf}"

response=$(curl -s "${api_base}/job/add/paperoffice_aiocr___generate" \
  -H "Authorization: Bearer ${api_key}" \
  -F "file_1=@${input_file}" \
  -F "ocr_mode=text" \
  -F "output_searchable_pdf=true" \
  -F "priority=900")

# Evaluate result and extract PDF URL (check multiple possible field locations)
eval "$(echo "${response}" | python3 -c "
import sys, json
data = json.load(sys.stdin)
output = data.get('result', {}).get('output', {})
summary = output.get('summary', {})
pdf_url = (
    output.get('searchable_pdf_url', '')
    or summary.get('searchable_pdf_url', '')
    or summary.get('searchable_pdf_path', '')
    or output.get('download_url', '')
)
pdf_token = output.get('download_token', '') or summary.get('download_token', '')
print(f'fulltext=\"{summary.get(\"total_pages\", 0)} pages extracted\"')
print(f'pdf_url=\"{pdf_url}\"')
print(f'pdf_token=\"{pdf_token}\"')
")"

echo "Status: $(echo "${response}" | python3 -c "import sys,json; print(json.load(sys.stdin).get('status',''))")"
echo "${fulltext}"

if [ -n "${pdf_url}" ]; then
  echo "PDF download: ${pdf_url}"
  curl -s -o "${output_file}" \
    -H "Authorization: Bearer ${api_key}" \
    "${pdf_url}"
  echo "Saved: ${output_file}"
elif [ -n "${pdf_token}" ]; then
  echo "Download token: ${pdf_token}"
  curl -s -o "${output_file}" \
    -H "Authorization: Bearer ${api_key}" \
    "${api_base}/job/download/${pdf_token}"
  echo "Saved: ${output_file}"
else
  echo "No PDF download found in the response."
  echo "Full response:"
  echo "${response}" | python3 -m json.tool
fi
