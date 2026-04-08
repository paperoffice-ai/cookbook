#!/usr/bin/env python3
"""PaperOffice AI — Knowledge Graph aufbauen und abfragen"""
import os
import sys
import json
import requests

BASE_URL = "https://api.paperoffice.ai/latest/knowledge_graph"
API_KEY = os.environ.get("PAPEROFFICE_API_KEY", "")

BEISPIEL_TEXT = (
    "Die Mustermann GmbH hat ihren Hauptsitz in München. "
    "CEO ist Max Mustermann. Das Unternehmen wurde 2010 gegründet "
    "und beschäftigt 500 Mitarbeiter. Hauptkunde ist die Beispiel AG aus Berlin."
)


def build_graph(text: str) -> dict:
    """Erstellt einen Knowledge Graph aus Text."""
    if not API_KEY:
        raise ValueError("PAPEROFFICE_API_KEY nicht gesetzt")

    response = requests.post(
        f"{BASE_URL}/build",
        headers={"Authorization": f"Bearer {API_KEY}"},
        data={"text": text},
    )
    response.raise_for_status()
    return response.json()


def query_graph(graph_id: str, query: str) -> dict:
    """Stellt eine Frage an einen bestehenden Knowledge Graph."""
    if not API_KEY:
        raise ValueError("PAPEROFFICE_API_KEY nicht gesetzt")

    response = requests.post(
        f"{BASE_URL}/query",
        headers={"Authorization": f"Bearer {API_KEY}"},
        data={"graph_id": graph_id, "query": query},
    )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    text = sys.argv[1] if len(sys.argv) > 1 else BEISPIEL_TEXT

    # Graph aufbauen
    print("=== Knowledge Graph aufbauen ===")
    print(f"Text: {text[:100]}...\n")

    build_result = build_graph(text)
    graph_id = build_result.get("graph_id", "")
    stats = build_result.get("stats", {})

    print(f"Graph-ID:  {graph_id}")
    print(f"Knoten:    {stats.get('nodes', '?')}")
    print(f"Kanten:    {stats.get('edges', '?')}")

    # Knoten anzeigen
    nodes = build_result.get("nodes", [])
    if nodes:
        print(f"\nKnoten ({len(nodes)}):")
        for node in nodes[:10]:
            print(f"  • {node.get('label', node.get('id', '?'))}")

    if not graph_id:
        print("\n⚠ Kein graph_id erhalten, Query übersprungen.")
        sys.exit(0)

    # Graph abfragen
    frage = "Wer ist der CEO der Mustermann GmbH?"
    print(f"\n=== Knowledge Graph abfragen ===")
    print(f"Frage: {frage}\n")

    query_result = query_graph(graph_id, frage)
    print(f"Antwort:    {query_result.get('answer', '?')}")
    print(f"Konfidenz:  {query_result.get('confidence', '?')}")

    relevant = query_result.get("relevant_nodes", [])
    if relevant:
        print(f"\nRelevante Knoten:")
        for node in relevant:
            print(f"  • {node.get('label', node.get('id', '?'))}")
