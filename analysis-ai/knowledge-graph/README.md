# Knowledge Graph — Build and query

Automatically creates a knowledge graph from unstructured text and enables natural language queries over the extracted relationships.

## Endpoints

```
POST https://api.paperoffice.ai/latest/knowledge_graph/build
POST https://api.paperoffice.ai/latest/knowledge_graph/query
```

**Authentication:** Bearer Token

## Parameters (build)

| Parameter | Type | Required | Description |
|---|---|---|---|
| `text` | string | ✅* | Text from which the graph is created |
| `document_id` | string | ✅* | Alternatively: ID of an already uploaded document |

\* Either `text` or `document_id` must be provided.

## Parameters (query)

| Parameter | Type | Required | Description |
|---|---|---|---|
| `graph_id` | string | ✅ | ID of the previously created graph |
| `query` | string | ✅ | Natural language question |

## How to run

```bash
export PAPEROFFICE_API_KEY=po_sk_xxx

# Bash
bash example.sh "The company XY is located in Berlin. The CEO is Mr. Meier."

# Python
pip install requests
python3 example.py

# Node.js (v18+)
node example.js
```

## Expected response (build)

```json
{
    "status": "success",
    "graph_id": "kg_123",
    "nodes": [
        { "id": "n1", "label": "Mustermann GmbH", "type": "organization" },
        { "id": "n2", "label": "München", "type": "location" },
        { "id": "n3", "label": "Max Mustermann", "type": "person" }
    ],
    "edges": [
        { "source": "n1", "target": "n2", "relation": "hat_sitz_in" },
        { "source": "n3", "target": "n1", "relation": "ist_ceo_von" }
    ],
    "stats": { "nodes": 15, "edges": 22 }
}
```

## Expected response (query)

```json
{
    "status": "success",
    "answer": "Max Mustermann ist der CEO der Mustermann GmbH.",
    "relevant_nodes": [
        { "id": "n3", "label": "Max Mustermann", "type": "person" },
        { "id": "n1", "label": "Mustermann GmbH", "type": "organization" }
    ],
    "confidence": 0.87
}
```

## How it works

1. **Build:** The text is analyzed, entities are extracted and relationships between them are identified. The result is a directed graph with nodes (entities) and edges (relationships).
2. **Query:** Natural language questions are resolved against the graph. The answer is based on the stored relationships and includes relevant nodes as evidence.

## Common use cases

- **Due diligence:** Extract business relationships from contracts and reports
- **Investigative research:** Uncover person networks and interconnections
- **Knowledge management:** Connect and make internal documents searchable
- **Compliance:** Analyze supply chain relationships and dependencies
