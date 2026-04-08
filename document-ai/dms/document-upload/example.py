#!/usr/bin/env python3
"""PaperOffice AI — Dokument ins DMS hochladen

Verwendung:
    export PAPEROFFICE_API_KEY=po_sk_xxx
    python3 example.py vertrag.pdf "Buchhaltung" "rechnung,2026,q1"
"""
import os
import sys
import requests

api_base = "https://api.paperoffice.ai/latest"
api_key = os.environ.get("PAPEROFFICE_API_KEY", "")


def document_upload(
    file_path: str,
    workspace_name: str,
    tags: str = "",
    description: str = "",
    token: str = api_key,
) -> dict:
    """Lädt ein Dokument in den angegebenen Workspace hoch."""
    if not token:
        raise ValueError("PAPEROFFICE_API_KEY nicht gesetzt")

    data = {"workspace_name": workspace_name}
    if tags:
        data["tags"] = tags
    if description:
        data["description"] = description

    with open(file_path, "rb") as f:
        response = requests.post(
            f"{api_base}/documents/upload",
            headers={"Authorization": f"Bearer {token}"},
            files={"file_1": f},
            data=data,
        )
    response.raise_for_status()
    return response.json()


def print_document_info(data: dict):
    """Gibt die Metadaten des hochgeladenen Dokuments aus."""
    doc = data.get("document", {})
    print(f"  ID:        {doc.get('id', '—')}")
    print(f"  Dateiname: {doc.get('filename', '—')}")
    print(f"  Workspace: {doc.get('workspace', '—')}")
    print(f"  Tags:      {doc.get('tags', [])}")
    print(f"  Größe:     {doc.get('size', '—')}")
    print(f"  Erstellt:  {doc.get('created_at', '—')}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("Verwendung: python3 example.py <datei> <workspace> [tags]")

    file_path = sys.argv[1]
    workspace = sys.argv[2]
    tags = sys.argv[3] if len(sys.argv) > 3 else ""

    print(f"→ Lade hoch: {file_path} → Workspace: {workspace}")
    result = document_upload(file_path, workspace, tags=tags)

    if result.get("status") == "success":
        print_document_info(result)
    else:
        print("Fehler:", result)
