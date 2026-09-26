# Windsurf — Auto-Classification System

**Tool:** Windsurf IDE | **Output:** Auto-Classification System with Folder Watch

## Prompt

Copy this prompt directly into Windsurf:

```
Read this API guide first, completely:
https://api.paperoffice.ai/latest/docs/llms.txt
Use the Postman collection at https://api.paperoffice.ai/latest/docs/postman only for exact request and response samples.

Build a document classifier that:
1. Watches a folder for new PDFs
2. Uses OCR (POST /job/add/paperoffice_aiocr___generate, ocr_mode=complete) to extract text
3. Classifies into: invoice, contract, receipt, correspondence
4. Moves files to category subfolders
5. Logs results to classification_log.csv

Use Bearer token for authentication.
Priority=900 for sync response.
```

## What you get

A classification system that:
- Watches a folder for new PDFs (Watchdog)
- Extracts text via OCR
- Automatically classifies documents (invoice, contract, receipt, correspondence)
- Moves files to category subfolders
- Maintains a CSV log

## Tips

- Bearer token required (`export PAPEROFFICE_API_KEY=po_ut_xxx`)
- `ocr_mode=complete` for text + tables
- `processing_lane=instant` for synchronous response
- Classification can be rule-based (keywords) or AI-based
