#!/usr/bin/env python3
"""PaperOffice AI — Entities of a processed document, grouped by type"""
import os
import sys
import requests

API_BASE = "https://api.paperoffice.ai/latest"
API_KEY = os.environ.get("PAPEROFFICE_API_KEY", "")


def get_document_entities(documents_id: int, entity_type: str = None, min_confidence: float = None) -> dict:
    """Returns the entities the AI-DMS extracted from a document (companies, persons, IBANs, amounts, dates ...)."""
    if not API_KEY:
        raise ValueError("PAPEROFFICE_API_KEY not set")

    params = {"documents_id": documents_id}
    if entity_type:
        params["type"] = entity_type
    if min_confidence is not None:
        params["min_confidence"] = min_confidence

    response = requests.get(
        f"{API_BASE}/document_intelligence/entities",
        headers={"Authorization": f"Bearer {API_KEY}"},
        params=params,
    )
    response.raise_for_status()
    return response.json()


def group_by_type(entities: list) -> dict:
    """Groups entities by type for clear output."""
    grouped = {}
    for entity in entities:
        grouped.setdefault(entity.get("type", "unknown"), []).append(entity)
    return grouped


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(f"Usage: {sys.argv[0]} <documents_id> [type] [min_confidence]\n"
                 "Find documents_id with POST /documents/document-search.")
    documents_id = int(sys.argv[1])
    entity_type = sys.argv[2] if len(sys.argv) > 2 else None
    min_conf = float(sys.argv[3]) if len(sys.argv) > 3 else None

    data = get_document_entities(documents_id, entity_type, min_conf)
    entities = data.get("entities", [])
    print(f"Document:   {data.get('file_name')} (id {data.get('document_id')})")
    print(f"Entities:   {data.get('total', len(entities))}\n")

    for typ, items in group_by_type(entities).items():
        print(f"[{typ}]")
        for e in items:
            conf = round(float(e.get("confidence", 0)) * 100)
            print(f"  • {str(e.get('value', '')).ljust(40)} ({conf}%)")
