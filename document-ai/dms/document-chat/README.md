# Chat with Documents (GraphRAG)

Ask natural language questions about your DMS documents and receive **AI-generated answers with evidence**. Powered by GraphRAG — the AI reads the document's knowledge graph and answers precisely based on the content.

## Endpoint

```
POST https://api.paperoffice.ai/latest/knowledge_graph/universe
```

**Authentication:** Bearer Token (API key required)

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `question` | string | **Yes** | Natural language question about the document |
| `pofid` | string | No | PaperOffice File ID — scope the query to a specific document |
| `max_hops` | int | No | Maximum relationship traversal depth (default: `3`) |
| `data_hints` | string | No | Additional context to guide the answer |

> **Note:** `pofid` is the PaperOffice File ID (a unique document identifier), not a numeric ID.
> You get the `pofid` from the document upload response or from the DMS document list.

## How to run

```bash
export PAPEROFFICE_API_KEY="your_api_key"

# Bash — single question about a specific document
bash example.sh "What is the termination period?" pofid_abc123

# Bash — question across all documents
bash example.sh "What is the termination period?"

# Python — single question
pip install requests
python3 example.py "What is the termination period?" pofid_abc123

# Node.js
node example.js "What is the termination period?" pofid_abc123
```

## Response structure

```json
{
    "status": "success",
    "answer": "The termination period is 3 months to the end of the quarter according to §5 para. 2 of the contract.",
    "relevant_nodes": [
        {
            "id": "n42",
            "label": "Termination Period",
            "type": "contract_term"
        },
        {
            "id": "n15",
            "label": "3 months",
            "type": "duration"
        }
    ],
    "confidence": 0.92
}
```

## How it works

Document Chat uses **GraphRAG** (Graph-based Retrieval-Augmented Generation):

1. **Knowledge Graph:** When a document is uploaded to the DMS, entities and relationships are automatically extracted into a knowledge graph
2. **Query:** Your natural language question is resolved against the graph using multi-hop reasoning
3. **Answer:** The AI generates a precise answer based on the graph data, including relevant evidence nodes

### Advantages over simple search

| Property | Keyword Search | Document Chat (GraphRAG) |
|---|---|---|
| Output | Text fragments | Formulated answer with reasoning |
| Evidence | No | Yes (relevant nodes with types) |
| Multi-hop reasoning | No | Yes (connects related facts) |
| Follow-up questions | No | Yes (include `data_hints` for context) |

## Tips

- **Precise questions** yield better answers than vague inquiries
- Use `pofid` to focus on a specific document, or omit to search across all documents
- Use `data_hints` to provide additional context (e.g., "This is a German lease contract")
- Increase `max_hops` for questions that require connecting distant facts
- Document must have been previously uploaded via [Document Upload](../document-upload/)

## See also

- [Knowledge Graph](../../../analysis-ai/knowledge-graph/) — Full knowledge graph API reference
- [Smart Search (RAG)](../smart-search/) — RAG-based document search
- [Entity Extraction](../../../analysis-ai/entity-extraction/) — Extract entities from documents
