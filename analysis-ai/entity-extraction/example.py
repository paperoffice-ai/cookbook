#!/usr/bin/env python3
"""PaperOffice AI — Entity extraction (NER) with grouping by type"""
import os
import sys
import requests

API_URL = "https://api.paperoffice.ai/latest/document_intelligence/entities"
API_KEY = os.environ.get("PAPEROFFICE_API_KEY", "")

EXAMPLE_TEXT = (
    "Acme Corporation, based in New York, signed a contract worth "
    "250,000 USD with Example Inc. on March 15, 2025. "
    "Contact person is John Smith, reachable at +1 212 555 0123."
)


def extract_entities(text: str, entity_types: list = None) -> dict:
    """Extracts named entities from a text."""
    if not API_KEY:
        raise ValueError("PAPEROFFICE_API_KEY not set")

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
    """Groups entities by type for clear output."""
    grouped = {}
    for entity in entities:
        typ = entity.get("type", "unknown")
        grouped.setdefault(typ, []).append(entity)
    return grouped


if __name__ == "__main__":
    text = sys.argv[1] if len(sys.argv) > 1 else EXAMPLE_TEXT

    print(f"=== Entity Extraction ===")
    print(f"Text: {text[:100]}...\n")

    result = extract_entities(text)
    entities = result.get("entities", [])

    print(f"Entities found: {len(entities)}\n")

    for typ, items in group_by_type(entities).items():
        print(f"--- {typ.upper()} ({len(items)}) ---")
        for e in items:
            conf = e.get("confidence", 0)
            print(f"  • {e['text']:<30} (Confidence: {conf:.0%})")
        print()
