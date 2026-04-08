#!/usr/bin/env python3
"""PaperOffice AI — AI-powered document generation

Usage:
    export PAPEROFFICE_API_KEY=po_sk_xxx
    python3 example.py "invoice_standard" pdf
"""
import os
import sys
import json
import requests

api_base = "https://api.paperoffice.ai/latest"
api_key = os.environ.get("PAPEROFFICE_API_KEY", "")


def document_generate(
    template: str,
    variables: dict = None,
    output_format: str = "pdf",
    token: str = api_key,
) -> dict:
    """Generates a document from a template with variables."""
    if not token:
        raise ValueError("PAPEROFFICE_API_KEY not set")

    data = {
        "template": template,
        "output_format": output_format,
    }
    if variables:
        data["variables"] = json.dumps(variables)

    response = requests.post(
        f"{api_base}/document_generation/generate",
        headers={"Authorization": f"Bearer {token}"},
        data=data,
    )
    response.raise_for_status()
    return response.json()


def download_document(url: str, output_path: str, token: str = api_key):
    """Downloads the generated document."""
    response = requests.get(
        url,
        headers={"Authorization": f"Bearer {token}"},
        stream=True,
    )
    response.raise_for_status()
    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"  Saved: {output_path}")


if __name__ == "__main__":
    template = sys.argv[1] if len(sys.argv) > 1 else None
    if not template:
        sys.exit("Usage: python3 example.py <template> [pdf|docx]")

    output_format = sys.argv[2] if len(sys.argv) > 2 else "pdf"

    variables = {
        "firma": "Muster GmbH",
        "rechnungsnummer": "2026-042",
        "betrag": "1.250,00",
        "datum": "08.04.2026",
    }

    print(f"→ Generating document from template: {template} ({output_format})")
    result = document_generate(template, variables=variables, output_format=output_format)

    if result.get("status") == "success":
        doc = result.get("document", {})
        print(f"  Download URL: {doc.get('download_url', '—')}")
        print(f"  Format:       {doc.get('format', '—')}")
        print(f"  Pages:        {doc.get('pages', '—')}")

        download_url = doc.get("download_url")
        if download_url:
            output_path = f"generated.{output_format}"
            download_document(download_url, output_path)
    else:
        print("Error:", result)
