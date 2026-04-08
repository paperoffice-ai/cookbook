#!/usr/bin/env bash
# PaperOffice AI — Durchsuchbare PDF erzeugen (OCR + Searchable PDF)

api_base="https://api.paperoffice.ai/latest"
api_key="${PAPEROFFICE_API_KEY:?Bitte PAPEROFFICE_API_KEY setzen}"
input_file="${1:?Bitte Dateipfad als Argument übergeben}"
output_file="${2:-searchable_output.pdf}"

response=$(curl -s "${api_base}/job/add/paperoffice_aiocr___generate" \
  -H "Authorization: Bearer ${api_key}" \
  -F "file_1=@${input_file}" \
  -F "ocr_mode=text" \
  -F "output_searchable_pdf=true" \
  -F "priority=900")

# Ergebnis auswerten und PDF-URL extrahieren
eval "$(echo "${response}" | python3 -c "
import sys, json
data = json.load(sys.stdin)
output = data.get('result', {}).get('output', {})
summary = output.get('summary', {})
pdf_url = output.get('searchable_pdf_url', '') or output.get('download_url', '')
pdf_token = output.get('download_token', '')
print(f'fulltext=\"{summary.get(\"total_pages\", 0)} Seiten extrahiert\"')
print(f'pdf_url=\"{pdf_url}\"')
print(f'pdf_token=\"{pdf_token}\"')
")"

echo "Status: $(echo "${response}" | python3 -c "import sys,json; print(json.load(sys.stdin).get('status',''))")"
echo "${fulltext}"

if [ -n "${pdf_url}" ]; then
  echo "PDF-Download: ${pdf_url}"
  curl -s -o "${output_file}" \
    -H "Authorization: Bearer ${api_key}" \
    "${pdf_url}"
  echo "Gespeichert: ${output_file}"
elif [ -n "${pdf_token}" ]; then
  echo "Download-Token: ${pdf_token}"
  curl -s -o "${output_file}" \
    -H "Authorization: Bearer ${api_key}" \
    "${api_base}/job/download/${pdf_token}"
  echo "Gespeichert: ${output_file}"
else
  echo "Kein PDF-Download in der Response gefunden."
  echo "Vollständige Response:"
  echo "${response}" | python3 -m json.tool
fi
