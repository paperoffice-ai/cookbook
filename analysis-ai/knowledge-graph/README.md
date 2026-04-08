# Knowledge Graph — Aufbau und Abfrage

Erstellt automatisch einen Knowledge Graph aus unstrukturiertem Text und ermöglicht natürlichsprachliche Abfragen über die extrahierten Zusammenhänge.

## Endpoints

```
POST https://api.paperoffice.ai/latest/knowledge_graph/build
POST https://api.paperoffice.ai/latest/knowledge_graph/query
```

**Authentifizierung:** Bearer Token

## Parameter (build)

| Parameter | Typ | Pflicht | Beschreibung |
|---|---|---|---|
| `text` | string | ✅* | Text, aus dem der Graph erstellt wird |
| `document_id` | string | ✅* | Alternativ: ID eines bereits hochgeladenen Dokuments |

\* Entweder `text` oder `document_id` muss angegeben werden.

## Parameter (query)

| Parameter | Typ | Pflicht | Beschreibung |
|---|---|---|---|
| `graph_id` | string | ✅ | ID des zuvor erstellten Graphs |
| `query` | string | ✅ | Natürlichsprachliche Frage |

## Ausführen

```bash
export PAPEROFFICE_API_KEY=po_sk_xxx

# Bash
bash example.sh "Die Firma XY sitzt in Berlin. CEO ist Herr Meier."

# Python
pip install requests
python3 example.py

# Node.js (v18+)
node example.js
```

## Erwartete Antwort (build)

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

## Erwartete Antwort (query)

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

## Funktionsweise

1. **Build:** Der Text wird analysiert, Entitäten extrahiert und Beziehungen zwischen ihnen erkannt. Das Ergebnis ist ein gerichteter Graph mit Knoten (Entitäten) und Kanten (Beziehungen).
2. **Query:** Natürlichsprachliche Fragen werden gegen den Graph aufgelöst. Die Antwort basiert auf den gespeicherten Zusammenhängen und enthält relevante Knoten als Beleg.

## Anwendungsfälle

- **Due Diligence:** Unternehmensbeziehungen aus Verträgen und Berichten extrahieren
- **Investigative Recherche:** Personen-Netzwerke und Verflechtungen aufdecken
- **Wissensmanagement:** Interne Dokumente vernetzen und durchsuchbar machen
- **Compliance:** Lieferketten-Beziehungen und Abhängigkeiten analysieren
