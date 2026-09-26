# Claude — Invoice Pipeline

**Tool:** Claude | **Output:** Complete Python script with Bounding Box Verification

## Prompt

Copy this prompt directly into Claude:

```
Read this API guide first, completely:
https://api.paperoffice.ai/latest/docs/llms.txt
Use the Postman collection at https://api.paperoffice.ai/latest/docs/postman only for exact request and response samples.

Create a Python script that:
1. Takes a folder of invoice PDFs
2. Extracts all fields using POST /job/add/workflow with idp_collection=invoice
3. Returns source_boxes for verification (position data per field)
4. Exports to CSV

Important: Use file_1 for uploads, model=premium.
Handle both HTTP 200 (inline result) and HTTP 202 (job_id, poll) responses.
```

## What you get

Claude generates a complete Python script that:
- Iterates through a folder of invoice PDFs
- Extracts each invoice via PaperOffice IDP
- Provides source boxes for visual review
- Exports results as CSV
- Correctly handles sync/async modes

## Tips

- Add `model=premium` for the best extraction quality
- `processing_lane = instant` returns the result inline when it finishes in time; otherwise HTTP 202 with `job_id` — poll `GET /job/get/{job_id}`
- Bearer token required (`export PAPEROFFICE_API_KEY=po_ut_xxx`)
