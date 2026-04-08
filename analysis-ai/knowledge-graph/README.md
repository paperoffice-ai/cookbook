# Knowledge Graph — Query, Visualize, and Analyze

Query and visualize the PaperOffice Knowledge Graph built from your DMS documents and connected data sources.

## Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/knowledge_graph/universe` | POST | **Main endpoint** — query, visualize (Mermaid), GraphRAG |
| `/knowledge_graph/stats` | GET | Graph statistics (node/edge counts) |
| `/knowledge_graph/partners` | GET | Business partner network |
| `/knowledge_graph/document_relations` | GET | Document relationship map |
| `/document_intelligence/knowledge_graph/{document_id}` | GET | Per-document knowledge graph |
| `/document_intelligence/knowledge_graph/{workspace_id}` | GET | Per-workspace knowledge graph |

**Authentication:** Bearer Token

> **Note:** The knowledge graph is automatically built from documents in your DMS.
> There is no separate "build" step — upload documents, and the graph grows.

## Parameters — `/knowledge_graph/universe`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `question` | string | No | Natural language question (triggers GraphRAG query) |
| `pofid` | string | No | PaperOffice File ID — scope the query to a specific document |
| `max_hops` | int | No | Maximum relationship hops (default: `3`) |
| `depth` | int | No | Graph traversal depth (for visualization) |
| `format` | string | No | Output format: `mermaid` for diagram syntax |
| `data_hints` | string | No | Additional context to guide the query |

### Usage patterns

| Action | Parameters |
|---|---|
| **Ask a question** | `question` (+ optional `pofid` to scope) |
| **Get Mermaid diagram** | `format=mermaid` (+ optional `depth`) |
| **GraphRAG ultra** | `question` + `pofid` + `data_hints` |

## Parameters — `/knowledge_graph/partners`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `workspace_id` | int | No | Restrict to a specific workspace |
| `query` | string | No | Filter partners by name/keyword |

## How to run

```bash
export PAPEROFFICE_API_KEY=po_sk_xxx

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
