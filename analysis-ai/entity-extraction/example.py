#!/usr/bin/env python3
"""PaperOffice AI — Entity-Extraktion (NER) mit Gruppierung nach Typ"""
import os
import sys
import requests

API_URL = "https://api.paperoffice.ai/latest/document_intelligence/entities"
API_KEY = os.environ.get("PAPEROFFICE_API_KEY", "")

BEISPIEL_TEXT = (
    "Die Mustermann GmbH mit Sitz in München hat am 15. März 2025 "
    "einen Vertrag über 250.000 EUR mit der Beispiel AG abgeschlossen. "
    "Ansprechpartner ist Max Mustermann, erreichbar unter +49 89 123456."
)


def extract_entities(text: str, entity_types: list = None) -> dict:
    """Extrahiert benannte Entitäten aus einem Text."""
    if not API_KEY:
        raise ValueError("PAPEROFFICE_API_KEY nicht gesetzt")

    payload = {"text": text}
    if entity_types:
        payload["entity_types"] = ",".join(entity_types)

    response = requests.post(
        API_URL,
        headers={"Authorization": f"Bearer {API_KEY}"},
        data=payload,
    )
    response.raise_for_status()
    return response.json()


def group_by_type(entities: list) -> dict:
    """Gruppiert Entitäten nach Typ für übersichtliche Ausgabe."""
    grouped = {}
    for entity in entities:
        typ = entity.get("type", "unknown")
        grouped.setdefault(typ, []).append(entity)
    return grouped


if __name__ == "__main__":
    text = sys.argv[1] if len(sys.argv) > 1 else BEISPIEL_TEXT

    print(f"=== Entity-Extraktion ===")
    print(f"Text: {text[:100]}...\n")

    result = extract_entities(text)
    entities = result.get("entities", [])

    print(f"Gefundene Entitäten: {len(entities)}\n")

    for typ, items in group_by_type(entities).items():
        print(f"--- {typ.upper()} ({len(items)}) ---")
        for e in items:
            conf = e.get("confidence", 0)
            print(f"  • {e['text']:<30} (Konfidenz: {conf:.0%})")
        print()
