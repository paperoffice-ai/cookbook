#!/usr/bin/env python3
"""PaperOffice AI — Knowledge Base complete CRUD cycle"""
import os
import sys
import json
import requests

BASE_URL = "https://api.paperoffice.ai/latest/knowledge"
API_KEY = os.environ.get("PAPEROFFICE_API_KEY", "")


def api_headers() -> dict:
    if not API_KEY:
        raise ValueError("PAPEROFFICE_API_KEY not set")
    return {"Authorization": f"Bearer {API_KEY}"}


def kb_list() -> dict:
    """List all knowledge bases."""
    r = requests.get(f"{BASE_URL}/kb_list", headers=api_headers())
    r.raise_for_status()
    return r.json()


def kb_create(name: str, description: str = "", language: str = "de") -> dict:
    """Create a new knowledge base."""
    r = requests.post(
        f"{BASE_URL}/kb_create",
        headers=api_headers(),
        data={"name": name, "description": description, "primary_language": language},
    )
    r.raise_for_status()
    return r.json()


def kb_update(kb_id: int, **kwargs) -> dict:
    """Update a knowledge base (name, description)."""
    payload = {"kb_id": kb_id, **kwargs}
    r = requests.post(f"{BASE_URL}/kb_update", headers=api_headers(), data=payload)
    r.raise_for_status()
    return r.json()


def kb_delete(kb_id: int) -> dict:
    """Delete a knowledge base."""
    r = requests.post(
        f"{BASE_URL}/kb_delete", headers=api_headers(), data={"kb_id": kb_id}
    )
    r.raise_for_status()
    return r.json()


def article_create(kb_id: int, title: str, content: str, category: str = "") -> dict:
    """Create an article in a KB."""
    payload = {"kb_id": kb_id, "title": title, "content": content}
    if category:
        payload["category"] = category
    r = requests.post(
        f"{BASE_URL}/article_create", headers=api_headers(), data=payload
    )
    r.raise_for_status()
    return r.json()


def article_list(kb_id: int) -> dict:
    """List all articles in a KB."""
    r = requests.get(
        f"{BASE_URL}/article_list", headers=api_headers(), params={"kb_id": kb_id}
    )
    r.raise_for_status()
    return r.json()


def article_update(article_id: int, **kwargs) -> dict:
    """Update an article (title, content)."""
    payload = {"article_id": article_id, **kwargs}
    r = requests.post(
        f"{BASE_URL}/article_update", headers=api_headers(), data=payload
    )
    r.raise_for_status()
    return r.json()


def article_delete(article_id: int) -> dict:
    """Delete an article."""
    r = requests.post(
        f"{BASE_URL}/article_delete",
        headers=api_headers(),
        data={"article_id": article_id},
    )
    r.raise_for_status()
    return r.json()


if __name__ == "__main__":
    # 1. Show existing KBs
    print("=== Existing Knowledge Bases ===")
    existing = kb_list()
    for kb in existing.get("data", []):
        print(f"  • [{kb['id']}] {kb['name']} ({kb['status']})")

    # 2. Create new KB
    print("\n=== Create new KB ===")
    created = kb_create("Cookbook-Test-KB", "Test data for cookbook example")
    kb_data = created.get("data", created)
    kb_id = kb_data.get("id", kb_data.get("kb_id"))
    print(f"  Created: ID={kb_id}")

    if not kb_id:
        print("⚠ No KB ID received.")
        sys.exit(1)

    # 3. Rename KB
    print("\n=== Rename KB ===")
    kb_update(kb_id, name="Cookbook-Test-KB-Updated")
    print(f"  Renamed: Cookbook-Test-KB → Cookbook-Test-KB-Updated")

    # 4. Add articles
    print("\n=== Create articles ===")
    art1 = article_create(
        kb_id,
        "Getting Started with PaperOffice",
        "PaperOffice AI provides intelligent document processing, OCR and knowledge management.",
        "Introduction",
    )
    art1_id = art1.get("data", art1).get("id", art1.get("article_id"))
    print(f"  Article 1: ID={art1_id}")

    art2 = article_create(
        kb_id,
        "API Authentication",
        "All API calls require a Bearer Token in the Authorization header.",
        "Technical",
    )
    art2_id = art2.get("data", art2).get("id", art2.get("article_id"))
    print(f"  Article 2: ID={art2_id}")

    # 5. List articles
    print("\n=== Articles in KB ===")
    articles = article_list(kb_id)
    for art in articles.get("data", []):
        print(f"  • [{art.get('id')}] {art.get('title')}")

    # 6. Update article
    if art1_id:
        print("\n=== Update article ===")
        article_update(art1_id, title="Getting Started (updated)")
        print(f"  Article {art1_id} updated.")

    # 7. Cleanup
    print("\n=== Cleanup — Delete KB ===")
    kb_delete(kb_id)
    print(f"  KB {kb_id} deleted.")

    print("\n✓ Complete CRUD cycle finished.")
