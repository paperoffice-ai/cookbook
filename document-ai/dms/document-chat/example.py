#!/usr/bin/env python3
"""PaperOffice AI — Chat mit einem Dokument (RAG)

Stellt Fragen an ein hochgeladenes Dokument. Die KI antwortet
basierend auf dem Dokumentinhalt mit Quellenangaben.

Verwendung:
    export PAPEROFFICE_API_KEY=po_sk_xxx
    python3 example.py 1234 "Was ist die Kündigungsfrist?"
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
    """Stellt eine Frage an ein Dokument und gibt die RAG-Antwort zurück."""
    if not token:
        raise ValueError("PAPEROFFICE_API_KEY nicht gesetzt")

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
    """Gibt Antwort und Quellen formatiert aus."""
    print()
    print("Antwort:")
    print(data.get("answer", "—"))
    print()

    sources = data.get("sources", [])
    if sources:
        print(f"Quellen ({len(sources)}):")
        print(f"{'Seite':<8} {'Konfidenz':<12} {'Text':<60}")
        print("─" * 82)
        for s in sources:
            page = str(s.get("page", "—"))
            conf = str(s.get("confidence", "—"))
            text = s.get("text", "")[:60]
            print(f"{page:<8} {conf:<12} {text}")


def interactive_chat(document_id: int):
    """Interaktiver Chat-Modus — mehrere Fragen nacheinander stellen."""
    print(f"Dokument-Chat (ID: {document_id}) — 'q' zum Beenden")
    print("─" * 50)

    while True:
        try:
            question = input("\nFrage: ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not question or question.lower() in ("q", "quit", "exit"):
            break

        result = document_chat(document_id, question)
        if result.get("status") == "success":
            print_answer(result)
        else:
            print("Fehler:", result)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Verwendung: python3 example.py <document_id> [frage]")

    doc_id = int(sys.argv[1])

    if len(sys.argv) > 2:
        question = sys.argv[2]
        print(f"→ Frage an Dokument {doc_id}: {question}")
        result = document_chat(doc_id, question)
        if result.get("status") == "success":
            print_answer(result)
        else:
            print("Fehler:", result)
    else:
        interactive_chat(doc_id)
