#!/usr/bin/env python3
"""PaperOffice AI — Upload document to DMS

Usage:
    export PAPEROFFICE_API_KEY=po_sk_xxx
    python3 example.py contract.pdf "Accounting" "invoice,2026,q1"
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
    """Uploads a document to the specified workspace."""
    if not token:
        raise ValueError("PAPEROFFICE_API_KEY not set")

    data = {"workspace_name": workspace_name}
    if tags:
        data["tags"] = tags
    if description:
        data["description"] = description

    with open(file_path, "rb") as f:
        response = requests.post(
            f"{api_base}/documents/document-put",
            headers={"Authorization": f"Bearer {token}"},
            files={"file": (os.path.basename(file_path), f)},
            data=data,
        )
    response.raise_for_status()
    return response.json()


def print_document_info(data: dict):
    """Prints the metadata of the uploaded document."""
    doc = data.get("document", {})
    print(f"  ID:        {doc.get('id', '—')}")
    print(f"  Filename:  {doc.get('filename', '—')}")
    print(f"  Workspace: {doc.get('workspace', '—')}")
    print(f"  Tags:      {doc.get('tags', [])}")
    print(f"  Size:      {doc.get('size', '—')}")
    print(f"  Created:   {doc.get('created_at', '—')}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("Usage: python3 example.py <file> <workspace> [tags]")

    file_path = sys.argv[1]
    workspace = sys.argv[2]
    tags = sys.argv[3] if len(sys.argv) > 3 else ""

    print(f"→ Uploading: {file_path} → Workspace: {workspace}")
    result = document_upload(file_path, workspace, tags=tags)

    if result.get("status") == "success":
        print_document_info(result)
    else:
        print("Error:", result)
