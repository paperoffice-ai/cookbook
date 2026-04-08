# Async Job Polling — Submit, Poll, Result

For larger files or lower priorities, the PaperOffice AI API works asynchronously. This workflow demonstrates the 3-step process: Submit job → Poll status → Retrieve result.

## Endpoints

| Step | Method | Endpoint |
|---|---|---|
| Submit | POST | `/job/add/{pipeline}` |
| Poll | GET | `/job/get/{job_id}` |
| Download | GET | `/job/download/{token}` (if file result) |

**Authentication:** Bearer Token for all endpoints

## Sync vs. Async

The `priority` parameter controls the processing mode:

| Priority | Mode | Behavior | SLA |
|---|---|---|---|
| `≥ 900` | **Synchronous** | Result directly in the response | ~20s |
| `500–599` | **Async (standard)** | Returns `job_id`, poll for result | ~30 min |
| `100–499` | **Async (low)** | Background queue, lower cost | Best effort |

> **Important:** Higher priority = faster processing but higher credit cost.

## Step 1: Submit job

```bash
curl -X POST "https://api.paperoffice.ai/latest/job/add/paperoffice_aiocr___generate" \
  -H "Authorization: Bearer $PAPEROFFICE_API_KEY" \
  -F "file_1=@document.pdf" \
  -F "ocr_mode=text" \
  -F "priority=500"
```

Response:

```json
{
  "status": "success",
  "job_id": "poai-job_500_1775674797.5357_93d126ea",
  "message": "Job queued for processing",
  "operation": "aiocr",
  "pipeline": "paperoffice_aiocr___generate"
}
```

## Step 2: Poll status

```bash
curl -s "https://api.paperoffice.ai/latest/job/get/poai-job_500_1775674797.5357_93d126ea" \
  -H "Authorization: Bearer $PAPEROFFICE_API_KEY"
```

While processing:

```json
{
  "status": "success",
  "job_status": "processing",
  "job_id": "poai-job_500_1775674797.5357_93d126ea",
  "progress": 45
}
```

Possible `job_status` values:

| Status | Action |
|---|---|
| `queued` | Keep polling |
| `processing` | Keep polling |
| `completed` | Done — result is in the response |
| `failed` | Error — check `error` field |
| `waiting` | Waiting for resources — keep polling |

## Step 3: Retrieve result

When `job_status` is `completed`:

```json
{
  "status": "success",
  "job_status": "completed",
  "job_id": "poai-job_500_1775674797.5357_93d126ea",
  "job_result": {
    "result": { },
    "output_files": [
      "https://api.paperoffice.ai/latest/job/download/..."
    ]
  }
}
```

> **Note:** Some pipelines (like Dataripper) return `job_result.result` as a JSON **string** — parse it with `JSON.parse()` / `json.loads()`.

## Polling flow diagram

```
POST /job/add/... (priority=500)
  └─→ {"status":"success", "job_id":"poai-job_500_abc123"}

GET /job/get/poai-job_500_abc123
  └─→ {"job_status":"queued"}        ← keep polling (wait 2s)
  └─→ {"job_status":"processing"}    ← keep polling (wait 2s)
  └─→ {"job_status":"completed", "job_result":{...}}  ← done!
```

## How to run

```bash
export PAPEROFFICE_API_KEY="your_api_key"

# Bash
chmod +x example.sh && ./example.sh /path/to/file.pdf

# Python
pip install requests
python3 example.py /path/to/file.pdf

# Node.js (v18+)
node example.js /path/to/file.pdf
```

## Tips

- **Polling interval:** 2 seconds is a good starting value. For large files consider 5s.
- **Timeout:** Abort after 300 seconds (5 min) for standard priority, 60s for high priority.
- **Exponential backoff:** Start at 2s, increase to 5s, 10s to reduce API calls.
- **Webhooks:** For production use, consider [webhooks](../webhooks/) instead of polling.
- **Download files:** Use `job_result.output_files[0]` for file-producing jobs (PDF, audio, images).

## See also

- [Webhooks](../webhooks/) — Get notified instead of polling
- [Hello World](../hello-world/) — Synchronous API call basics
