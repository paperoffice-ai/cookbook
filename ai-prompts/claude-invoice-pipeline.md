# Claude — Invoice Pipeline

**Tool:** Claude | **Output:** Complete Python script with Bounding Box Verification

## Prompt

Copy this prompt directly into Claude:

```
Read this API documentation:
https://api.paperoffice.ai/latest/docs/postman

Create a Python script that:
1. Takes a folder of invoice PDFs
2. Extracts all fields using POST /job/add/workflow with idp_collection=invoice
3. Returns source_boxes for verification (position data per field)
4. Exports to CSV

Important: Use file_1 for uploads, model=premium.
Handle both sync (priority>=900) and async modes.
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
- `priority >= 900` = synchronous response, `< 900` = async with polling
- Bearer token required (`export PAPEROFFICE_API_KEY=po_sk_xxx`)
