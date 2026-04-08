#!/usr/bin/env python3
"""PaperOffice AI — Chat with documents via GraphRAG

Ask natural language questions about DMS documents using the knowledge graph.
Uses POST /knowledge_graph/universe with question + optional pofid.
"""
import os
import sys
import json
import requests

api_base = "https://api.paperoffice.ai/latest"
API_KEY = os.environ.get("PAPEROFFICE_API_KEY", "")


def chat_with_document(question: str, pofid: str = "", max_hops: int = 3) -> dict:
    """Ask a question about a document via GraphRAG."""
    if not API_KEY:
        raise ValueError("PAPEROFFICE_API_KEY not set")

    payload = {"question": question, "max_hops": max_hops}
    if pofid:
        payload["pofid"] = pofid

    response = requests.post(
        f"{api_base}/knowledge_graph/universe",
        headers={"Authorization": f"Bearer {API_KEY}"},
        data=payload,
    )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <question> [pofid]")
        sys.exit(1)

    question = sys.argv[1]
    pofid = sys.argv[2] if len(sys.argv) > 2 else ""

    print(f"Question: {question}")
    if pofid:
        print(f"Document: {pofid}")
    print()

    result = chat_with_document(question, pofid=pofid)

    answer = result.get("answer", "(no answer)")
    print(f"Answer: {answer}")

    confidence = result.get("confidence")
    if confidence:
        print(f"Confidence: {confidence}")

    nodes = result.get("relevant_nodes", [])
    if nodes:
        print(f"\nEvidence ({len(nodes)} nodes):")
        for node in nodes[:5]:
            label = node.get("label", node.get("id", "?"))
            ntype = node.get("type", "?")
            print(f"  - {label} ({ntype})")
