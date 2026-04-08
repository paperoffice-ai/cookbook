#!/usr/bin/env python3
"""PaperOffice AI — Knowledge Base semantische Suche mit formatierter Ausgabe"""
import os
import sys
import requests

API_URL = "https://api.paperoffice.ai/latest/knowledge/search"
API_KEY = os.environ.get("PAPEROFFICE_API_KEY", "")


def kb_search(query: str, kb_id: int = None, limit: int = 5) -> dict:
    """Semantische Suche über Knowledge-Base-Artikel."""
    if not API_KEY:
        raise ValueError("PAPEROFFICE_API_KEY nicht gesetzt")

    payload = {"query": query, "limit": limit}
    if kb_id:
        payload["kb_id"] = kb_id

    response = requests.post(
        API_URL,
        headers={"Authorization": f"Bearer {API_KEY}"},
        data=payload,
    )
    response.raise_for_status()
    return response.json()


def print_results(results: list):
    """Formatierte Ausgabe der Suchergebnisse mit Score-Balken."""
    if not results:
        print("  Keine Ergebnisse gefunden.")
        return

    for i, r in enumerate(results, 1):
        score = r.get("score", 0)
        bar_length = int(score * 20)
        bar = "█" * bar_length + "░" * (20 - bar_length)

        print(f"  {i}. {r.get('title', 'Ohne Titel')}")
        print(f"     Score: [{bar}] {score:.0%}")
        snippet = r.get("snippet", "")
        if snippet:
            print(f"     {snippet[:120]}...")
        print()


if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "Wie funktioniert die API-Authentifizierung?"
    kb_id = int(sys.argv[2]) if len(sys.argv) > 2 else None

    print(f"=== Knowledge Base Suche ===")
    print(f"Frage: {query}")
    if kb_id:
        print(f"KB-ID: {kb_id}")
    print()

    result = kb_search(query, kb_id=kb_id)
    results = result.get("results", [])

    print(f"Treffer: {len(results)}\n")
    print_results(results)
