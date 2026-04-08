# Chat with documents (Document Intelligence)

Asks questions about an uploaded document and receives **AI-generated answers with source references**. Based on RAG (Retrieval-Augmented Generation) — the AI reads the document and answers precisely based on the content.

## Endpoint

```
POST https://api.paperoffice.ai/latest/document_intelligence/chat
```

**Authentication:** Bearer Token (API key required)

## Parameters

| Parameter        | Required | Description                                       |
|------------------|----------|---------------------------------------------------|
| `document_id`    | Yes      | ID of the document (from upload response)          |
| `question`       | Yes      | Question about the document (natural language)     |
| `context_window` | No       | Context window size (more = broader context)       |

## How to run

```bash
export PAPEROFFICE_API_KEY="your_api_key"

# Bash — single question
bash example.sh 1234 "What is the termination period?"

# Python — single question
pip install requests
python3 example.py 1234 "What is the termination period?"

# Python — interactive mode
python3 example.py 1234

# Node.js
node example.js 1234 "What is the termination period?"
```

## Response structure

```json
{
  "status": "success",
  "answer": "The termination period is 3 months to the end of the quarter according to §5 para. 2 of the contract.",
  "sources": [
    {
      "page": 3,
      "text": "The contract duration is 12 months. The termination period is 3 months...",
      "confidence": "high"
    }
  ]
}
```

## Document Intelligence (RAG concept)

Document Intelligence combines two steps:

1. **Retrieval** — The most relevant passages in the document are identified
2. **Generation** — The AI formulates an answer based on the found passages

### Advantages over simple search

| Property            | Search             | Document Chat                |
|---------------------|--------------------|------------------------------|
| Output              | Text fragments     | Formulated answer            |
| Source references    | No                 | Yes (page, text, confidence) |
| Summary             | No                 | Yes                          |
| Follow-up questions | No                 | Yes (context is preserved)   |

## Source references

Each answer contains `sources` with:

| Field         | Description                                |
|---------------|--------------------------------------------|
| `page`        | Page number in the document                |
| `text`        | Relevant text excerpt                      |
| `confidence`  | Confidence: `high`, `medium`, `low`        |

## Tips

- **Precise questions** yield better answers than vague inquiries
- **Interactive mode** (Python) allows follow-up questions about the same document
- **context_window** — increase for questions that need context across multiple pages
- Document must have been previously uploaded via `document-upload/`
- Works with PDF, DOCX, images and all supported formats
