#!/usr/bin/env python3
"""PaperOffice AI — Intelligente Dokumentensuche im DMS

Verwendung:
    export PAPEROFFICE_API_KEY=po_sk_xxx
    python3 example.py "Vertragsbedingungen" "Buchhaltung"
"""
import os
import sys
import requests

api_base = "https://api.paperoffice.ai/latest"
api_key = os.environ.get("PAPEROFFICE_API_KEY", "")


def document_search(
    query: str,
    workspace_name: str = "",
    limit: int = 10,
    offset: int = 0,
    token: str = api_key,
) -> dict:
    """Führt eine semantische Suche im DMS durch."""
    if not token:
        raise ValueError("PAPEROFFICE_API_KEY nicht gesetzt")

    data = {"global_search": query, "limit": limit, "offset": offset}
    if workspace_name:
        data["workspace_name"] = workspace_name

    response = requests.post(
        f"{api_base}/documents/search",
        headers={"Authorization": f"Bearer {token}"},
        data=data,
    )
    response.raise_for_status()
    return response.json()


def print_results(data: dict):
    """Formatierte Ausgabe der Suchergebnisse."""
    results = data.get("results", [])
    total = data.get("total", len(results))

    print(f"Treffer: {total}")
    print()
    print(f"{'ID':<8} {'Dateiname':<35} {'Score':<10} {'Workspace':<20}")
    print("─" * 75)

    for r in results:
        doc_id = str(r.get("id", "—"))
        filename = r.get("filename", "—")
        score = str(r.get("score", "—"))
        workspace = r.get("workspace", "—")
        print(f"{doc_id:<8} {filename:<35} {score:<10} {workspace:<20}")

        snippet = r.get("snippet", "")
        if snippet:
            print(f"         {snippet[:100]}")
            print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Verwendung: python3 example.py <suchbegriff> [workspace] [limit]")

    query = sys.argv[1]
    workspace = sys.argv[2] if len(sys.argv) > 2 else ""
    limit = int(sys.argv[3]) if len(sys.argv) > 3 else 10

    print(f"→ Suche nach: {query}")
    result = document_search(query, workspace_name=workspace, limit=limit)

    if result.get("status") == "success":
        print_results(result)
    else:
        print("Fehler:", result)
