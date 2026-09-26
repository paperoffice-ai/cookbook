# Knowledge Graph — Ask, Statistics, Partners

Query the PaperOffice Knowledge Graph built from the documents in a workspace: ask questions with cited sources, read statistics, list business partners.

## Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/knowledge_graph/ask` | POST | **Ask a question** — answer with `sources` (documents_id, file_name) |
| `/knowledge_graph/stats` | GET | Graph statistics (`workspace_id`) |
| `/knowledge_graph/partners` | GET | Business partner network (`workspace_id`) |
| `/knowledge_graph/partner/{name}` | GET | One partner and all its documents |
| `/knowledge_graph/business_case/{ref}` | GET | Business case by reference number (e.g. invoice number) |
| `/knowledge_graph/timeline` | GET | Chronological document view |
| `/knowledge_graph/universe` | GET | Universe view over all data sources (`format=mermaid` for a diagram) |
| `/knowledge_graph/document/{id}` | GET | Relations of one document |

**Authentication:** Bearer token. Group tokens (`po_gt_`) must pass `workspace_id`.

> The graph is built automatically when documents are processed. There is no separate build step.

## Parameters — `POST /knowledge_graph/ask`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `question` | string | Yes | Natural-language question (at least 5 characters, about documents/workspaces/partners) |
| `workspace_id` | int | Yes for group tokens | Workspace to answer from |
| `pofid` | string | No | Scope the question to one document |
| `data_hints` | array | No | e.g. `["document"]` |

Response: `answer`, `routing` (`harvester_graph_rag` or `agent`), `sources[]`, `verified_facts[]`, `warnings[]`. Off-topic questions are rejected with `OUT_OF_DOMAIN_QUESTION_REJECTED`.

## How to run

```bash
export PAPEROFFICE_API_KEY=po_ut_xxx

bash example.sh 24 "Who issued invoice RE-2026-7834?"
python3 example.py 24 "Who issued invoice RE-2026-7834?"
node example.js 24 "Who issued invoice RE-2026-7834?"
```

## Parameters — `/knowledge_graph/partners`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `workspace_id` | int | No | Restrict to a specific workspace |
| `query` | string | No | Filter partners by name/keyword |

## How to run

```bash
export PAPEROFFICE_API_KEY=po_ut_xxx

# Bash
bash example.sh "Who is the CEO of Acme Corporation?"
bash example.sh "Show supplier relationships" doc_abc123

# Python
pip install requests
python3 example.py "What contracts mention delivery terms?"

# Node.js (v18+)
node example.js "Who are the main business partners?"
```

## Expected response (query)

```json
{
    "status": "success",
    "answer": "John Smith is the CEO of Acme Corporation, as stated in the annual report.",
    "relevant_nodes": [
        { "id": "n3", "label": "John Smith", "type": "person" },
        { "id": "n1", "label": "Acme Corporation", "type": "organization" }
    ],
    "confidence": 0.87
}
```

## Expected response (Mermaid)

```json
{
    "status": "success",
    "format": "mermaid",
    "graph": "graph TD\n  A[Acme Corp] -->|headquartered_in| B[New York]\n  C[John Smith] -->|is_ceo_of| A"
}
```

## Expected response (stats)

```json
{
    "status": "success",
    "stats": {
        "total_nodes": 1234,
        "total_edges": 5678,
        "node_types": { "person": 120, "organization": 89, "location": 45 },
        "edge_types": { "works_at": 200, "located_in": 150 }
    }
}
```

## How it works

1. **Automatic graph building:** When documents are uploaded to the DMS, entities and relationships are extracted automatically — no manual build step required.
2. **Query:** Natural language questions are resolved against the graph using GraphRAG. The answer includes relevant nodes as evidence.
3. **Visualization:** Request `format=mermaid` to get a diagram you can render in any Mermaid-compatible viewer.

## Common use cases

- **Due diligence:** Extract business relationships from contracts and reports
- **Investigative research:** Uncover person networks and interconnections
- **Knowledge management:** Connect and make internal documents searchable
- **Compliance:** Analyze supply chain relationships and dependencies
- **AI pipelines:** Use GraphRAG queries to enrich LLM context with structured knowledge
