# Batch PDF Split — 3000 Seiten

**Tool:** Beliebiges AI-Tool | **Output:** Batch Processor für 3000-Seiten PDFs

## Prompt

```
Read this API documentation:
https://api.paperoffice.ai/latest/docs/postman

Create a batch processor that:
1. Takes a folder of large PDFs (up to 3000 pages each)
2. Uses POST /job with template=pdf_ai_split
3. Uses naming_instruction for smart filenames
4. Handles async jobs with polling (priority<900)

Use locale=de_DE for German document types.
```

## Was du bekommst

Ein Batch-Processor der:
- Einen Ordner mit großen PDFs durcharbeitet
- Jedes PDF via AI in Einzeldokumente splittet
- Intelligente Dateinamen generiert (Dokumenttyp + Datum + Absender)
- Async-Modus mit Polling für große Dateien nutzt
- Deutsche Dokumenttypen korrekt erkennt

## Tipps

- `priority < 900` für async Verarbeitung (empfohlen bei großen PDFs)
- `naming_instruction` als Freitext: z.B. `"Dokumenttyp_Datum_Absender"`
- `locale=de_DE` für deutsche Dokumenttyp-Erkennung
