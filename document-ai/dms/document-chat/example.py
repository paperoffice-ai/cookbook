#!/usr/bin/env python3
"""PaperOffice AI — Chat with a document (RAG)

Asks questions about an uploaded document. The AI answers
based on the document content with source references.

Usage:
    export PAPEROFFICE_API_KEY=po_sk_xxx
    python3 example.py 1234 "What is the termination period?"
"""
import os
import sys
import requests

api_base = "https://api.paperoffice.ai/latest"
api_key = os.environ.get("PAPEROFFICE_API_KEY", "")


def document_chat(
    document_id: int,
    question: str,
    context_window: int = None,
    token: str = api_key,
) -> dict:
    """Asks a question about a document and returns the RAG answer."""
    if not token:
        raise ValueError("PAPEROFFICE_API_KEY not set")

    data = {"document_id": document_id, "question": question}
    if context_window is not None:
        data["context_window"] = context_window

    response = requests.post(
        f"{api_base}/document_intelligence/chat",
        headers={"Authorization": f"Bearer {token}"},
        data=data,
    )
    response.raise_for_status()
    return response.json()


def print_answer(data: dict):
    """Prints answer and sources in formatted output."""
    print()
    print("Answer:")
    print(data.get("answer", "—"))
    print()

    sources = data.get("sources", [])
    if sources:
        print(f"Sources ({len(sources)}):")
        print(f"{'Page':<8} {'Confidence':<12} {'Text':<60}")
        print("─" * 82)
        for s in sources:
            page = str(s.get("page", "—"))
            conf = str(s.get("confidence", "—"))
            text = s.get("text", "")[:60]
            print(f"{page:<8} {conf:<12} {text}")


def interactive_chat(document_id: int):
    """Interactive chat mode — ask multiple questions in sequence."""
    print(f"Document chat (ID: {document_id}) — 'q' to quit")
    print("─" * 50)

    while True:
        try:
            question = input("\nQuestion: ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not question or question.lower() in ("q", "quit", "exit"):
            break

        result = document_chat(document_id, question)
        if result.get("status") == "success":
            print_answer(result)
        else:
            print("Error:", result)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python3 example.py <document_id> [question]")

    doc_id = int(sys.argv[1])

    if len(sys.argv) > 2:
        question = sys.argv[2]
        print(f"→ Question to document {doc_id}: {question}")
        result = document_chat(doc_id, question)
        if result.get("status") == "success":
            print_answer(result)
        else:
            print("Error:", result)
    else:
        interactive_chat(doc_id)
