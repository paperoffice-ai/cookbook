#!/usr/bin/env bash
# PaperOffice AI — Convert PDF to Office formats (DOCX, XLSX, PPTX)
#
# Pipeline: paperoffice_dataripper___pdf2office
# Output formats: docx (default), xlsx, pptx
#
# Always async — conversion requires processing time.

set -euo pipefail

api_base="https://api.paperoffice.ai/latest"
api_key="${PAPEROFFICE_API_KEY:?Please set PAPEROFFICE_API_KEY}"
input_file="${1:?Please provide PDF file path as argument}"
output_format="${2:-docx}"

if [ ! -f "${input_file}" ]; then
  echo "Error: File not found: ${input_file}"
  exit 1
fi

# Step 1: Submit conversion job (always async)
echo ">>> Submitting pdf2office job: ${input_file} → ${output_format}"

submit_response=$(curl -s -X POST "${api_base}/job/add/paperoffice_dataripper___pdf2office" \
  -H "Authorization: Bearer ${api_key}" \
  -F "file=@${input_file}" \
  -F "output_format=${output_format}" \
  -F "processing_lane=sla_1h")

job_id=$(echo "${submit_response}" | python3 -c "
import sys, json
data = json.load(sys.stdin)
if data.get('status') != 'success':
    print('', end='')
    sys.exit(0)
print(data.get('job_id', ''))
")

if [ -z "${job_id}" ]; then
  echo "Error: Job submission failed"
  echo "${submit_response}" | python3 -m json.tool
  exit 1
fi

eta=$(echo "${submit_response}" | python3 -c "
import sys, json
eta = json.load(sys.stdin).get('eta', {})
print(f\"ETA: {eta.get('estimated_completion', '?')} (queue pos: {eta.get('queue_position', '?')})\")
")
echo "Job submitted: ${job_id}"
echo "${eta}"

# Step 2: Poll until completed (longer intervals — conversion takes 30-90s)
echo ">>> Waiting for conversion..."
max_attempts=60
attempt=0
interval=5

while [ ${attempt} -lt ${max_attempts} ]; do
  attempt=$((attempt + 1))
  sleep ${interval}

  poll_response=$(curl -s "${api_base}/job/get/${job_id}" \
    -H "Authorization: Bearer ${api_key}")

  job_status=$(echo "${poll_response}" | python3 -c "
import sys, json
d = json.load(sys.stdin)
jr = d.get('job_result', {})
print(jr.get('status', d.get('job_status', 'unknown')))
")

  echo "  Attempt ${attempt}/${max_attempts}: ${job_status}"

  if [ "${job_status}" = "completed" ]; then
    # Download URL is at job_result.output_files[0] (not inside result)
    download_url=$(echo "${poll_response}" | python3 -c "
import sys, json
d = json.load(sys.stdin)
jr = d.get('job_result', {})
of = jr.get('output_files', [])
if of:
    print(of[0])
")

    if [ -n "${download_url}" ]; then
      output_name="${input_file%.*}.${output_format}"
      curl -s "${download_url}" \
        -H "Authorization: Bearer ${api_key}" \
        -o "${output_name}"
      echo "Saved as: ${output_name}"
    else
      echo "Conversion completed (check response for download details):"
      echo "${poll_response}" | python3 -c "
import sys, json
d = json.load(sys.stdin)
if '_billing' in d: del d['_billing']
print(json.dumps(d, indent=2)[:2000])
"
    fi
    exit 0
  fi

  if [ "${job_status}" = "failed" ] || [ "${job_status}" = "error" ]; then
    echo "Conversion failed!"
    echo "${poll_response}" | python3 -m json.tool
    exit 1
  fi

  if [ ${attempt} -eq 5 ]; then interval=10; fi
done

echo "Timeout: Conversion not completed after ${max_attempts} attempts"
exit 1
