#!/usr/bin/env python3
"""PaperOffice AI — Knowledge Base vollständiger CRUD-Zyklus"""
import os
import sys
import json
import requests

BASE_URL = "https://api.paperoffice.ai/latest/knowledge"
API_KEY = os.environ.get("PAPEROFFICE_API_KEY", "")


def api_headers() -> dict:
    if not API_KEY:
        raise ValueError("PAPEROFFICE_API_KEY nicht gesetzt")
    return {"Authorization": f"Bearer {API_KEY}"}


def kb_list() -> dict:
    """Alle Knowledge Bases auflisten."""
    r = requests.get(f"{BASE_URL}/kb_list", headers=api_headers())
    r.raise_for_status()
    return r.json()


def kb_create(name: str, description: str = "", language: str = "de") -> dict:
    """Neue Knowledge Base erstellen."""
    r = requests.post(
        f"{BASE_URL}/kb_create",
        headers=api_headers(),
        data={"name": name, "description": description, "primary_language": language},
    )
    r.raise_for_status()
    return r.json()


def kb_update(kb_id: int, **kwargs) -> dict:
    """Knowledge Base aktualisieren (name, description)."""
    payload = {"kb_id": kb_id, **kwargs}
    r = requests.post(f"{BASE_URL}/kb_update", headers=api_headers(), data=payload)
    r.raise_for_status()
    return r.json()


def kb_delete(kb_id: int) -> dict:
    """Knowledge Base löschen."""
    r = requests.post(
        f"{BASE_URL}/kb_delete", headers=api_headers(), data={"kb_id": kb_id}
    )
    r.raise_for_status()
    return r.json()


def article_create(kb_id: int, title: str, content: str, category: str = "") -> dict:
    """Artikel in einer KB erstellen."""
    payload = {"kb_id": kb_id, "title": title, "content": content}
    if category:
        payload["category"] = category
    r = requests.post(
        f"{BASE_URL}/article_create", headers=api_headers(), data=payload
    )
    r.raise_for_status()
    return r.json()


def article_list(kb_id: int) -> dict:
    """Alle Artikel einer KB auflisten."""
    r = requests.get(
        f"{BASE_URL}/article_list", headers=api_headers(), params={"kb_id": kb_id}
    )
    r.raise_for_status()
    return r.json()


def article_update(article_id: int, **kwargs) -> dict:
    """Artikel aktualisieren (title, content)."""
    payload = {"article_id": article_id, **kwargs}
    r = requests.post(
        f"{BASE_URL}/article_update", headers=api_headers(), data=payload
    )
    r.raise_for_status()
    return r.json()


def article_delete(article_id: int) -> dict:
    """Artikel löschen."""
    r = requests.post(
        f"{BASE_URL}/article_delete",
        headers=api_headers(),
        data={"article_id": article_id},
    )
    r.raise_for_status()
    return r.json()


if __name__ == "__main__":
    # 1. Bestehende KBs anzeigen
    print("=== Bestehende Knowledge Bases ===")
    existing = kb_list()
    for kb in existing.get("data", []):
        print(f"  • [{kb['id']}] {kb['name']} ({kb['status']})")

    # 2. Neue KB erstellen
    print("\n=== Neue KB erstellen ===")
    created = kb_create("Cookbook-Test-KB", "Testdaten für Cookbook-Beispiel")
    kb_data = created.get("data", created)
    kb_id = kb_data.get("id", kb_data.get("kb_id"))
    print(f"  Erstellt: ID={kb_id}")

    if not kb_id:
        print("⚠ Keine KB-ID erhalten.")
        sys.exit(1)

    # 3. KB umbenennen
    print("\n=== KB umbenennen ===")
    kb_update(kb_id, name="Cookbook-Test-KB-Updated")
    print(f"  Umbenannt: Cookbook-Test-KB → Cookbook-Test-KB-Updated")

    # 4. Artikel hinzufügen
    print("\n=== Artikel erstellen ===")
    art1 = article_create(
        kb_id,
        "Erste Schritte mit PaperOffice",
        "PaperOffice AI bietet intelligente Dokumentenverarbeitung, OCR und Knowledge Management.",
        "Einführung",
    )
    art1_id = art1.get("data", art1).get("id", art1.get("article_id"))
    print(f"  Artikel 1: ID={art1_id}")

    art2 = article_create(
        kb_id,
        "API-Authentifizierung",
        "Alle API-Aufrufe benötigen einen Bearer Token im Authorization-Header.",
        "Technik",
    )
    art2_id = art2.get("data", art2).get("id", art2.get("article_id"))
    print(f"  Artikel 2: ID={art2_id}")

    # 5. Artikel auflisten
    print("\n=== Artikel in KB ===")
    articles = article_list(kb_id)
    for art in articles.get("data", []):
        print(f"  • [{art.get('id')}] {art.get('title')}")

    # 6. Artikel aktualisieren
    if art1_id:
        print("\n=== Artikel aktualisieren ===")
        article_update(art1_id, title="Erste Schritte (aktualisiert)")
        print(f"  Artikel {art1_id} aktualisiert.")

    # 7. Aufräumen
    print("\n=== Aufräumen — KB löschen ===")
    kb_delete(kb_id)
    print(f"  KB {kb_id} gelöscht.")

    print("\n✓ Vollständiger CRUD-Zyklus abgeschlossen.")
