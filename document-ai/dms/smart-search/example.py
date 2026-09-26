#!/usr/bin/env python3
"""PaperOffice AI — Smart document search in DMS (Ultimate Search)

Usage:
    export PAPEROFFICE_API_KEY=po_ut_xxx
    python3 example.py "contract terms" 42
    python3 example.py "invoice 2026" 42 20
"""
import os
import sys
import json
import requests

api_base = "https://api.paperoffice.ai/latest"
api_key = os.environ.get("PAPEROFFICE_API_KEY", "")


def document_search(
    query: str,
    workspace_id: int,
    limit: int = 20,
    search_mode: str = "intelligent",
    search_preference: str = "balanced",
    token: str = api_key,
) -> dict:
    """Performs an Ultimate Search in the DMS."""
    if not token:
        raise ValueError("PAPEROFFICE_API_KEY not set")

    payload = {
        "workspace_id": workspace_id,
        "global_search": query,
        "search_mode": search_mode,
        "search_preference": search_preference,
        "limit": limit,
    }

    response = requests.post(
        f"{api_base}/documents/documents-list",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json=payload,
    )
    response.raise_for_status()
    return response.json()


def print_results(data: dict):
    """Formatted output of search results."""
    results = data.get("results", data.get("data", []))
    total = data.get("total", len(results))

    print(f"Hits: {total}")
    print()
    print(f"{'ID':<8} {'Filename':<35} {'Score':<10}")
    print("-" * 55)

    for r in results:
        doc_id = str(r.get("id", "-"))
        filename = r.get("filename", r.get("file_name", "-"))
        score = str(r.get("score", "-"))
        print(f"{doc_id:<8} {filename:<35} {score:<10}")

        snippet = r.get("snippet", "")
        if snippet:
            print(f"         {snippet[:100]}")
            print()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("Usage: python3 example.py <search_term> <workspace_id> [limit]")

    query = sys.argv[1]
    workspace_id = int(sys.argv[2])
    limit = int(sys.argv[3]) if len(sys.argv) > 3 else 20

    print(f"-> Searching for: {query} (workspace {workspace_id})")
    result = document_search(query, workspace_id=workspace_id, limit=limit)

    if result.get("status") == "success":
        print_results(result)
    else:
        print("Error:", json.dumps(result, indent=2))
