#!/usr/bin/env bash
# PaperOffice AI — Async Job Polling (Submit → Poll → Result)

api_base="https://api.paperoffice.ai/latest"
api_key="${PAPEROFFICE_API_KEY:?Please set PAPEROFFICE_API_KEY}"
input_file="${1:?Error: Please provide file path as argument}"

# Step 1: Submit job (processing_lane=sla_1h → async)
echo ">>> Submitting job..."
submit_response=$(curl -s "${api_base}/job/add/paperoffice_aiocr___generate" \
  -H "Authorization: Bearer ${api_key}" \
  -F "file_1=@${input_file}" \
  -F "ocr_mode=text" \
  -F "processing_lane=sla_1h")

job_id=$(echo "${submit_response}" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(data.get('job_id', ''))
")

if [ -z "${job_id}" ]; then
  echo "Error: No job_id received"
  echo "${submit_response}" | python3 -m json.tool
  exit 1
fi

echo "Job submitted: ${job_id}"

# Step 2: Poll status until completed
echo ">>> Waiting for result..."
max_attempts=30
attempt=0

while [ ${attempt} -lt ${max_attempts} ]; do
  attempt=$((attempt + 1))
  sleep 2

  poll_response=$(curl -s "${api_base}/job/get/${job_id}" \
    -H "Authorization: Bearer ${api_key}")

  status=$(echo "${poll_response}" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(data.get('job_status', 'unknown'))  # queued | processing | completed | failed
")

  echo "  Attempt ${attempt}/${max_attempts}: ${status}"

  if [ "${status}" = "completed" ]; then
    echo ""
    echo "--- Result ---"
    echo "${poll_response}" | python3 -m json.tool
    exit 0
  fi

  if [ "${status}" = "failed" ] || [ "${status}" = "error" ]; then
    echo "Job failed!"
    echo "${poll_response}" | python3 -m json.tool
    exit 1
  fi
done

echo "Timeout: Job not completed after ${max_attempts} attempts"
exit 1
