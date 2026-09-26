# OCR Data Extraction — Tables + Structured Data

**Tool:** Any AI Tool | **Output:** Complete OCR pipeline with table extraction and structured output

## Prompt

```
Read this API documentation:
https://api.paperoffice.ai/latest/docs/postman

Create a Node.js (ESM) script that:
1. Takes a scanned PDF as input
2. Runs OCR via POST /job/add/paperoffice_aiocr___generate with:
   - file_1 = the PDF
   - ocr_mode = complete (extracts text + bounding boxes + tables + layout)
   - processing_lane = instant (inline result on 200; on 202 poll job/get)
3. Parses the response:
   - Full text: result.output.summary.poaiocr_extracted_fulltext
   - Per-page text: result.output.pages["00001"].ocr_text
   - Per-page confidence: result.output.pages["00001"].confidence_avg
   - Bounding boxes: result.output.pages["00001"].bounding_boxes (array of word-level boxes with coordinates)
   - Tables: result.output.pages["00001"].tables (if present)
   - Language: result.output.pages["00001"].language.primary
4. Outputs a structured JSON with all extracted data
5. Also generates a searchable PDF if output_searchable_pdf=true

Use native fetch and FormData (Node.js 18+).
Bearer token from $PAPEROFFICE_API_KEY.
```

## What you get

A complete OCR extraction pipeline that:
- Extracts text with word-level bounding box coordinates
- Identifies tables with cell positions
- Detects page language and confidence scores
- Optionally creates a searchable PDF layer
- Outputs structured JSON for downstream processing

## Tips

- `ocr_mode=text` for fastest extraction (text only, no boxes)
- `ocr_mode=grid` for text + bounding boxes (no tables)
- `ocr_mode=complete` for full extraction (text + boxes + tables + layout)
- Max 200 pages per job on standard tier, 500 on premium
- Bounding boxes include `x`, `y`, `width`, `height` coordinates relative to page dimensions
- Add `locale=de_DE` for German-optimized OCR (affects date/number parsing)
