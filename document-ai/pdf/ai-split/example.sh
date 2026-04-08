#!/usr/bin/env bash
# PaperOffice AI — Intelligent PDF splitting with AI detection

api_base="https://api.paperoffice.ai/latest"
api_key="${PAPEROFFICE_API_KEY:?Please set PAPEROFFICE_API_KEY}"
input_file="${1:?Please provide file path as argument}"

# Upload PDF and split using AI
response=$(curl -s "${api_base}/job/add/workflow" \
  -H "Authorization: Bearer ${api_key}" \
  -F "file_1=@${input_file}" \
  -F "template=pdf_ai_split" \
  -F "naming_instruction=Name by document type and date" \
  -F "priority=900")

status=$(echo "${response}" | python3 -c "import sys,json; print(json.load(sys.stdin).get('status',''))")
echo "Status: ${status}"

if [ "${status}" != "success" ]; then
  echo "Error:"
  echo "${response}" | python3 -m json.tool
  exit 1
fi

# List split documents
echo ""
echo "--- Split documents ---"
echo "${response}" | python3 -c "
import sys, json
data = json.load(sys.stdin)
docs = data.get('result', {}).get('documents', [])
files = data.get('result', {}).get('files', [])
print(f'Number of sub-documents: {len(docs)}')
print()
for i, doc in enumerate(docs):
    print(f'  [{i+1}] {doc.get(\"suggested_filename\", \"unknown\")}')
    print(f'      Type:   {doc.get(\"document_type\", \"?\")}')
    print(f'      Pages:  {doc.get(\"page_range\", \"?\")}')
    print(f'      Date:   {doc.get(\"date\", \"?\")}')
    print(f'      Reason: {doc.get(\"reasoning\", \"\")}')
    if i < len(files):
        print(f'      URL:    {files[i]}')
    print()
"

# Download first sub-document
download_url=$(echo "${response}" | python3 -c "
import sys, json
files = json.load(sys.stdin).get('result', {}).get('files', [])
if files: print(files[0])
")

filename=$(echo "${response}" | python3 -c "
import sys, json
docs = json.load(sys.stdin).get('result', {}).get('documents', [])
if docs: print(docs[0].get('suggested_filename', 'part_1.pdf'))
")

if [ -n "${download_url}" ]; then
  curl -s "${download_url}" \
    -H "Authorization: Bearer ${api_key}" \
    -o "${filename}"
  echo "Downloaded: ${filename}"
fi
