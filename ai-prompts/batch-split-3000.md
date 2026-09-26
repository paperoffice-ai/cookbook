# Batch PDF Split — 3000 Pages

**Tool:** Any AI Tool | **Output:** Batch Processor for 3000-page PDFs

## Prompt

```
Read this API documentation:
https://api.paperoffice.ai/latest/docs/postman

Create a batch processor that:
1. Takes a folder of large PDFs (up to 3000 pages each)
2. Uses POST /job/add/workflow with template=pdf_ai_split
3. Uses naming_instruction for smart filenames
4. Handles HTTP 202 responses with polling (`GET /job/get/{job_id}`)

Use locale=de_DE for German document types.
```

## What you get

A batch processor that:
- Processes a folder of large PDFs
- Splits each PDF into individual documents via AI
- Generates smart filenames (document type + date + sender)
- Uses async mode with polling for large files
- Correctly recognizes German document types

## Tips

- `processing_lane = sla_1h` for large PDFs (response carries `job_id`; poll for the result)
- `naming_instruction` as free text: e.g. `"Dokumenttyp_Datum_Absender"`
- `locale=de_DE` for German document type recognition
