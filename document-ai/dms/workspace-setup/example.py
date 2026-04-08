#!/usr/bin/env python3
"""PaperOffice AI — Workspace erstellen & auflisten

Verwendung:
    export PAPEROFFICE_API_KEY=po_sk_xxx
    python3 example.py "Buchhaltung" "Rechnungen und Belege"
"""
import os
import sys
import requests

api_base = "https://api.paperoffice.ai/latest"
api_key = os.environ.get("PAPEROFFICE_API_KEY", "")


def workspace_create(name: str, description: str = "", token: str = api_key) -> dict:
    """Erstellt einen neuen Workspace im DMS."""
    if not token:
        raise ValueError("PAPEROFFICE_API_KEY nicht gesetzt")

    response = requests.post(
        f"{api_base}/documents/workspace_create",
        headers={"Authorization": f"Bearer {token}"},
        data={"name": name, "description": description},
    )
    response.raise_for_status()
    return response.json()


def workspace_list(token: str = api_key) -> dict:
    """Gibt alle verfügbaren Workspaces zurück."""
    if not token:
        raise ValueError("PAPEROFFICE_API_KEY nicht gesetzt")

    response = requests.get(
        f"{api_base}/documents/workspace_list",
        headers={"Authorization": f"Bearer {token}"},
    )
    response.raise_for_status()
    return response.json()


def print_workspaces(data: dict):
    """Formatierte Ausgabe der Workspace-Liste."""
    workspaces = data.get("workspaces", [])
    print(f"Gefunden: {len(workspaces)} Workspace(s)")
    print()
    print(f"{'ID':<8} {'Name':<30} {'Beschreibung':<40}")
    print("─" * 80)
    for ws in workspaces:
        ws_id = str(ws.get("id", "—"))
        name = ws.get("name", "—")
        desc = ws.get("description", "")
        print(f"{ws_id:<8} {name:<30} {desc:<40}")


if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "Mein Workspace"
    desc = sys.argv[2] if len(sys.argv) > 2 else "Automatisch erstellter Workspace"

    print(f"→ Erstelle Workspace: {name}")
    result = workspace_create(name, desc)

    if result.get("status") == "success":
        ws = result.get("workspace", {})
        print(f"  ID:           {ws.get('id', '—')}")
        print(f"  Name:         {ws.get('name', '—')}")
        print(f"  Beschreibung: {ws.get('description', '—')}")
        print(f"  Erstellt:     {ws.get('created_at', '—')}")
    else:
        print("Fehler:", result)

    print()
    print("→ Alle Workspaces auflisten")
    list_data = workspace_list()
    print_workspaces(list_data)
