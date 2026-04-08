#!/usr/bin/env python3
"""PaperOffice AI — Build and query knowledge graph"""
import os
import sys
import json
import requests

BASE_URL = "https://api.paperoffice.ai/latest/knowledge_graph"
API_KEY = os.environ.get("PAPEROFFICE_API_KEY", "")

EXAMPLE_TEXT = (
    "Die Mustermann GmbH hat ihren Hauptsitz in München. "
    "CEO ist Max Mustermann. Das Unternehmen wurde 2010 gegründet "
    "und beschäftigt 500 Mitarbeiter. Hauptkunde ist die Beispiel AG aus Berlin."
)


def build_graph(text: str) -> dict:
    """Creates a knowledge graph from text."""
    if not API_KEY:
        raise ValueError("PAPEROFFICE_API_KEY not set")

    response = requests.post(
        f"{BASE_URL}/build",
        headers={"Authorization": f"Bearer {API_KEY}"},
        data={"text": text},
    )
    response.raise_for_status()
    return response.json()


def query_graph(graph_id: str, query: str) -> dict:
    """Asks a question against an existing knowledge graph."""
    if not API_KEY:
        raise ValueError("PAPEROFFICE_API_KEY not set")

    response = requests.post(
        f"{BASE_URL}/query",
        headers={"Authorization": f"Bearer {API_KEY}"},
        data={"graph_id": graph_id, "query": query},
    )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    text = sys.argv[1] if len(sys.argv) > 1 else EXAMPLE_TEXT

    # Build graph
    print("=== Build knowledge graph ===")
    print(f"Text: {text[:100]}...\n")

    build_result = build_graph(text)
    graph_id = build_result.get("graph_id", "")
    stats = build_result.get("stats", {})

    print(f"Graph ID:  {graph_id}")
    print(f"Nodes:     {stats.get('nodes', '?')}")
    print(f"Edges:     {stats.get('edges', '?')}")

    # Display nodes
    nodes = build_result.get("nodes", [])
    if nodes:
        print(f"\nNodes ({len(nodes)}):")
        for node in nodes[:10]:
            print(f"  • {node.get('label', node.get('id', '?'))}")

    if not graph_id:
        print("\n⚠ No graph_id received, skipping query.")
        sys.exit(0)

    # Query graph
    question = "Wer ist der CEO der Mustermann GmbH?"
    print(f"\n=== Query knowledge graph ===")
    print(f"Question: {question}\n")

    query_result = query_graph(graph_id, question)
    print(f"Answer:     {query_result.get('answer', '?')}")
    print(f"Confidence: {query_result.get('confidence', '?')}")

    relevant = query_result.get("relevant_nodes", [])
    if relevant:
        print(f"\nRelevant nodes:")
        for node in relevant:
            print(f"  • {node.get('label', node.get('id', '?'))}")
