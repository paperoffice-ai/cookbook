# Knowledge Base Search — Semantic Article Search

Searches knowledge base articles using semantic search. Unlike keyword search, semantic search also finds matches that have the same meaning but use different words.

## Endpoint

```
POST https://api.paperoffice.ai/latest/knowledge/search
```

**Authentication:** Bearer Token

## Parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `query` | string | **Yes** | — | Search query in natural language |
| `kb_id` | int | No | all | Restrict search to a specific knowledge base |
| `language` | string | No | all | Language filter (`de`, `en`, `es`, `fr`, `it`, `pt`) |
| `limit` | int | No | `5` | Max number of results |
| `min_similarity` | float | No | — | Minimum similarity score (0.0–1.0) — filters out low-relevance results |
| `mode` | string | No | — | Search mode override |

## How to Run

```bash
export PAPEROFFICE_API_KEY=po_sk_xxx

# Bash — simple search
bash example.sh "How does OCR work?"

# Bash — search in specific KB with limit
bash example.sh "How does OCR work?" 9 3

# Python
pip install requests
python3 example.py "How does OCR work?"

# Node.js (v18+)
node example.js "How does OCR work?"
```

## Expected Response

```json
{
    "status": "success",
    "results": [
        {
            "article_id": 1,
            "title": "OCR Basics",
            "snippet": "Optical Character Recognition (OCR) converts images of text into machine-readable text...",
            "score": 0.92
        },
        {
            "article_id": 5,
            "title": "Document Processing",
            "snippet": "Document processing uses OCR as a first step to extract text from scanned documents...",
            "score": 0.78
        }
    ]
}
```

## Scoring

| Score Range | Meaning |
|---|---|
| 0.90 – 1.00 | Very high relevance — direct matches |
| 0.70 – 0.89 | High relevance — topically relevant |
| 0.50 – 0.69 | Medium relevance — related topic |
| < 0.50 | Low relevance — only distantly related |

## Semantic vs. Keyword

| Search Query | Keyword Search | Semantic Search |
|---|---|---|
| "How do I scan documents?" | Only finds articles containing "scan" or "documents" | Also finds articles about OCR, document processing, IDP |
| "Process invoice" | Only finds exact word matches | Also finds articles about invoice processing, receipt capture |

## Use Cases

- **Helpdesk AI:** Find relevant FAQ articles for customer inquiries
- **Chatbot:** Use context-relevant knowledge articles as a basis for answers
- **Internal search:** Provide employees with relevant documentation
- **RAG pipeline:** Retrieval-Augmented Generation with knowledge base context
