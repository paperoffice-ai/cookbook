#!/usr/bin/env python3
"""PaperOffice AI — Query and visualize knowledge graph"""
import os
import sys
import json
import requests

BASE_URL = "https://api.paperoffice.ai/latest/knowledge_graph"
API_KEY = os.environ.get("PAPEROFFICE_API_KEY", "")


def api_headers() -> dict:
    if not API_KEY:
        raise ValueError("PAPEROFFICE_API_KEY not set")
    return {"Authorization": f"Bearer {API_KEY}"}


def get_stats() -> dict:
    """Get knowledge graph statistics."""
    r = requests.get(f"{BASE_URL}/stats", headers=api_headers())
    r.raise_for_status()
    return r.json()


def query_graph(question: str, pofid: str = "", max_hops: int = 3) -> dict:
    """Ask a natural language question against the knowledge graph."""
    payload = {"question": question, "max_hops": max_hops}
    if pofid:
        payload["pofid"] = pofid
    r = requests.post(f"{BASE_URL}/universe", headers=api_headers(), data=payload)
    r.raise_for_status()
    return r.json()


def get_mermaid(pofid: str = "", depth: int = 3) -> dict:
    """Get knowledge graph as Mermaid diagram."""
    payload = {"format": "mermaid", "depth": depth}
    if pofid:
        payload["pofid"] = pofid
    r = requests.post(f"{BASE_URL}/universe", headers=api_headers(), data=payload)
    r.raise_for_status()
    return r.json()


def get_partners(workspace_id: int = None, query: str = "") -> dict:
    """Get business partner network."""
    params = {}
    if workspace_id:
        params["workspace_id"] = workspace_id
    if query:
        params["query"] = query
    r = requests.get(f"{BASE_URL}/partners", headers=api_headers(), params=params)
    r.raise_for_status()
    return r.json()


if __name__ == "__main__":
    question = sys.argv[1] if len(sys.argv) > 1 else "Who are the main business partners?"
    pofid = sys.argv[2] if len(sys.argv) > 2 else ""

    # 1. Graph statistics
    print("=== Graph statistics ===")
    stats = get_stats()
    print(json.dumps(stats, indent=2))

    # 2. Query the graph
    print(f"\n=== Query: {question} ===")
    if pofid:
        print(f"Scoped to document: {pofid}")
    result = query_graph(question, pofid=pofid)
    print(f"Answer:     {result.get('answer', '?')}")
    print(f"Confidence: {result.get('confidence', '?')}")

    relevant = result.get("relevant_nodes", [])
    if relevant:
        print(f"\nRelevant nodes ({len(relevant)}):")
        for node in relevant[:10]:
            print(f"  - {node.get('label', node.get('id', '?'))} ({node.get('type', '?')})")

    # 3. Mermaid visualization
    print("\n=== Mermaid diagram ===")
    mermaid = get_mermaid(pofid=pofid)
    graph_str = mermaid.get("graph", "")
    if graph_str:
        print(graph_str[:500])
    else:
        print(json.dumps(mermaid, indent=2))

    # 4. Business partners
    print("\n=== Business partners ===")
    partners = get_partners()
    print(json.dumps(partners, indent=2))
