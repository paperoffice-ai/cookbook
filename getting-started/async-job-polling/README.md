# Async Job Polling — Submit, Poll, Result

For larger files or lower priorities, the PaperOffice AI API works asynchronously. This workflow demonstrates the 3-step process: Submit job → Poll status → Retrieve result.

## Endpoints

| Step    | Method | Endpoint                                           |
|---------|--------|----------------------------------------------------|
| Submit  | POST   | `/job/add/paperoffice_aiocr___generate`             |
| Poll    | GET    | `/job/get/{job_id}`                                 |
| Download| GET    | `/job/download/{token}` (if file result)            |

**Authentication:** Bearer Token for all endpoints

## Sync vs. Async

The difference lies in the `priority`:

| Priority | Mode         | Behavior                                       |
|---------|--------------|-------------------------------------------------|
| `900`   | **Synchronous** | Result directly in the response               |
| `500`   | **Async**    | Returns `job_id`, result must be polled          |
| `100`   | **Low**      | Background queue, longer wait time               |

## Polling flow

```
POST /job/add/... (priority=500)
  └─→ {"status":"success", "job_id":"poai-job_500_abc123"}

GET /job/get/poai-job_500_abc123
  └─→ {"status":"processing"}     ← keep polling
  └─→ {"status":"queued"}         ← keep polling
  └─→ {"status":"completed", "result":{...}}  ← done!
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

- **Polling interval:** 2 seconds is a good starting value. For large files consider increasing to 5s.
- **Timeout:** Abort after 60 seconds and notify the user.
- **Webhooks:** Instead of polling you can also use webhooks — see the `webhooks/` recipe.
