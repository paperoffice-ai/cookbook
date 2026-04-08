#!/usr/bin/env bash
# PaperOffice AI — GDPR-compliant anonymization of documents
#
# Template: document_anonymize | Param: file (not file_1!)
# Categories: all, names, addresses, phone, email, iban, tax_id

api_base="https://api.paperoffice.ai/latest"
api_key="${PAPEROFFICE_API_KEY:?Please set PAPEROFFICE_API_KEY}"
input_file="${1:?Please provide file path as argument}"
redact_categories="${2:-all}"

echo "→ Anonymizing: ${input_file} (categories: ${redact_categories})"

response=$(curl -s "${api_base}/job/add/workflow" \
  -H "Authorization: Bearer ${api_key}" \
  -F "template=document_anonymize" \
  -F "file=@${input_file}" \
  -F "redact_categories=${redact_categories}" \
  -F "priority=900")

status=$(echo "${response}" | python3 -c "import sys,json; print(json.load(sys.stdin).get('status',''))")
echo "Status: ${status}"

if [ "${status}" != "success" ]; then
  echo "Error:"
  echo "${response}" | python3 -m json.tool
  exit 1
fi

download_url=$(echo "${response}" | python3 -c "
import sys, json
result = json.load(sys.stdin).get('result', {})
urls = result.get('anonymized_pdf', result.get('files', []))
if urls: print(urls[0])
")

if [ -n "${download_url}" ]; then
  curl -s "${download_url}" \
    -H "Authorization: Bearer ${api_key}" \
    -o "anonymized.pdf"
  echo "Downloaded: anonymized.pdf"
else
  echo "Error: No download URL received"
  exit 1
fi
