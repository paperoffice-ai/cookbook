#!/usr/bin/env python3
"""PaperOffice AI — Knowledge Graph: statistics, question, business partners"""
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


def get_stats(workspace_id: int) -> dict:
    """Graph statistics for one workspace."""
    r = requests.get(f"{BASE_URL}/stats", headers=api_headers(), params={"workspace_id": workspace_id})
    r.raise_for_status()
    return r.json()


def ask(question: str, workspace_id: int, pofid: str = "") -> dict:
    """Ask a natural-language question. The answer cites the source documents."""
    payload = {"question": question, "workspace_id": workspace_id}
    if pofid:
        payload["pofid"] = pofid
    r = requests.post(f"{BASE_URL}/ask", headers=api_headers(), json=payload, timeout=180)
    r.raise_for_status()
    return r.json()


def get_partners(workspace_id: int, query: str = "") -> dict:
    """Business partner network of a workspace."""
    params = {"workspace_id": workspace_id}
    if query:
        params["query"] = query
    r = requests.get(f"{BASE_URL}/partners", headers=api_headers(), params=params)
    r.raise_for_status()
    return r.json()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(f"Usage: {sys.argv[0]} <workspace_id> [question] [pofid]")
    workspace_id = int(sys.argv[1])
    question = sys.argv[2] if len(sys.argv) > 2 else "Who are the main business partners?"
    pofid = sys.argv[3] if len(sys.argv) > 3 else ""

    print("=== Graph statistics ===")
    print(json.dumps(get_stats(workspace_id).get("stats", {}), indent=2)[:800])

    print(f"\n=== Question: {question} ===")
    result = ask(question, workspace_id, pofid)
    print(f"Answer:  {result.get('answer', '')}")
    print(f"Routing: {result.get('routing')}")
    for src in result.get("sources", [])[:5]:
        print(f"  source: {src.get('file_name')} (documents_id {src.get('documents_id')})")

    print("\n=== Business partners ===")
    for p in get_partners(workspace_id).get("partners", [])[:10]:
        print(f"  - {p.get('name')}: {p.get('document_count')} documents")
