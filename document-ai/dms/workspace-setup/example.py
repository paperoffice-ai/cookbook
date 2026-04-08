#!/usr/bin/env python3
"""PaperOffice AI — Create & list workspaces

Usage:
    export PAPEROFFICE_API_KEY=po_sk_xxx
    python3 example.py "Accounting" "Invoices and receipts"
"""
import os
import sys
import requests

api_base = "https://api.paperoffice.ai/latest"
api_key = os.environ.get("PAPEROFFICE_API_KEY", "")


def workspace_create(name: str, description: str = "", token: str = api_key) -> dict:
    """Creates a new workspace in the DMS."""
    if not token:
        raise ValueError("PAPEROFFICE_API_KEY not set")

    response = requests.post(
        f"{api_base}/documents/workspace-create",
        headers={"Authorization": f"Bearer {token}"},
        data={"name": name, "description": description},
    )
    response.raise_for_status()
    return response.json()


def workspace_list(token: str = api_key) -> dict:
    """Returns all available workspaces."""
    if not token:
        raise ValueError("PAPEROFFICE_API_KEY not set")

    response = requests.get(
        f"{api_base}/documents/workspaces-list",
        headers={"Authorization": f"Bearer {token}"},
    )
    response.raise_for_status()
    return response.json()


def print_workspaces(data: dict):
    """Formatted output of the workspace list."""
    workspaces = data.get("workspaces", [])
    print(f"Found: {len(workspaces)} workspace(s)")
    print()
    print(f"{'ID':<8} {'Name':<30} {'Description':<40}")
    print("─" * 80)
    for ws in workspaces:
        ws_id = str(ws.get("id", "—"))
        name = ws.get("name", "—")
        desc = ws.get("description", "")
        print(f"{ws_id:<8} {name:<30} {desc:<40}")


if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "My Workspace"
    desc = sys.argv[2] if len(sys.argv) > 2 else "Automatically created workspace"

    print(f"→ Creating workspace: {name}")
    result = workspace_create(name, desc)

    if result.get("status") == "success":
        ws = result.get("workspace", {})
        print(f"  ID:          {ws.get('id', '—')}")
        print(f"  Name:        {ws.get('name', '—')}")
        print(f"  Description: {ws.get('description', '—')}")
        print(f"  Created:     {ws.get('created_at', '—')}")
    else:
        print("Error:", result)

    print()
    print("→ Listing all workspaces")
    list_data = workspace_list()
    print_workspaces(list_data)
