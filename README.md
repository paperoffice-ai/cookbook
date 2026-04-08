# PaperOffice AI Cookbook

Production-ready Recipes für die [PaperOffice AI API](https://paperoffice.ai) — OCR, IDP, PDF Split, TTS, MCP und mehr.

**Copy. Paste. Ship.**

---

## Quick Start

```bash
# 1. API-Key setzen
export PAPEROFFICE_API_KEY=po_sk_xxx

# 2. Recipe ausführen
cd quick-wins/ocr-oneliner
bash example.sh scan.png
```

Oder mit Python / Node.js:

```bash
pip install requests
python quick-wins/invoice-extractor/example.py invoice.pdf
```

---

## Recipes

### Quick Wins

Minimaler Code — sofort produktiv.

| Recipe | Was es tut | Sprachen |
|---|---|---|
| [Invoice Extractor](quick-wins/invoice-extractor/) | Rechnungsfelder + Bounding Boxes extrahieren | sh, py, js |
| [OCR One-Liner](quick-wins/ocr-oneliner/) | Text aus Bildern/PDFs | sh, py, js |
| [PDF Split 3000](quick-wins/pdf-split-3000/) | Sammel-PDFs splitten (bis 3000 Seiten) | sh, py, js |
| [GDPR Anonymizer](quick-wins/gdpr-anonymizer/) | PII erkennen und schwärzen | sh, py, js |
| [TTS Generator](quick-wins/tts-generator/) | Text → natürliche Sprache | sh, py, js |

### AI Prompts

Copy-Paste Prompts für Claude, Cursor, Windsurf & Co.

| Prompt | Tool | Output |
|---|---|---|
| [Claude Invoice Pipeline](ai-prompts/claude-invoice-pipeline.md) | Claude | Python-Script mit Batch-Verarbeitung |
| [Cursor MCP Setup](ai-prompts/cursor-mcp-setup.md) | Cursor IDE | MCP-Konfiguration + Document AI im Editor |
| [Voice Agent Builder](ai-prompts/voice-agent-builder.md) | Beliebig | Voice Agent mit TTS + STT |
| [Fraud Detection](ai-prompts/fraud-detection-system.md) | Beliebig | Device Fingerprint + IP Geolocation |
| [Batch PDF Split](ai-prompts/batch-split-3000.md) | Beliebig | Batch Processor für große PDFs |
| [Windsurf Classifier](ai-prompts/windsurf-classifier.md) | Windsurf | Auto-Classification mit Folder Watch |

### Real-World Use Cases

End-to-End Workflows für echte Probleme.

| Use Case | Beschreibung | Sprache |
|---|---|---|
| [AP Automation](use-cases/ap-automation/) | Eingangsrechnungen → Extraktion → CSV | Python |
| [Contract Analysis](use-cases/contract-analysis/) | Vertragsanalyse + Key Terms | Python |
| [PDF Converter](use-cases/pdf-converter/) | PDF → Word, PowerPoint, PDF/A | Python |
| [Webhook Pipeline](use-cases/webhook-pipeline/) | Echtzeit-Verarbeitung via Webhooks | Python |
| [Voice Documentation](use-cases/voice-documentation/) | Dokument → OCR → TTS → Audio | Python |
| [Batch OCR → CSV](use-cases/batch-ocr-csv/) | Ordner → OCR → CSV Export | Python |

### Pro Tips

→ [Pro Tips](pro-tips/) — Sync vs Async, Bounding Boxes, TTS-Stimmen, MCP, Retry-Strategien, Credit-System

---

## API-Endpoints

| Endpoint | Zweck |
|---|---|
| `POST /job/add/workflow` | Alle Datei-basierten Jobs (OCR, IDP, PDF-Split, Anonymisierung) |
| `POST /voice/tts` | Text-to-Speech |

```bash
# Beispiel: OCR
curl -X POST "https://api.paperoffice.ai/latest/job/add/workflow" \
  -H "Authorization: Bearer $PAPEROFFICE_API_KEY" \
  -F "file_1=@scan.png" -F "ocr_mode=complete" -F "priority=900"
```

## Authentifizierung

**Ein Bearer Token ist für alle Job-Endpoints erforderlich.**

```bash
export PAPEROFFICE_API_KEY=po_sk_xxx
```

Token erhältlich unter [paperoffice.ai](https://paperoffice.ai).

| Token-Typ | Prefix | Verwendung |
|---|---|---|
| System Key | `po_sk_` | Server-to-Server, voller Zugriff |
| User Token | `po_ut_` | User-scoped, abhängig von Lizenz |

> **Hinweis:** Ohne Token erhält man eine VISITOR-Session. Diese erlaubt nur `/ip2location`, `/currencyexchange`, `/health` und `/ping`. Alle Job/Processing-Endpoints (OCR, IDP, Voice, PDF, Image) benötigen einen Token.

---

## MCP Integration

PaperOffice bietet einen MCP-Server (Model Context Protocol) für native AI-Tool-Integration.

```json
{
  "mcpServers": {
    "paperoffice": {
      "url": "https://mcp.paperoffice.ai/cursor",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      }
    }
  }
}
```

| Client | URL |
|---|---|
| Cursor IDE | `https://mcp.paperoffice.ai/cursor` |
| Claude Desktop | `https://mcp.paperoffice.ai/claude` |
| Standard MCP | `https://mcp.paperoffice.ai/mcp` |
| OpenAI / ChatGPT | `https://mcp.paperoffice.ai/openai` |

---

## API-Dokumentation

Die vollständige API-Doku als Postman Collection:

```
https://api.paperoffice.ai/latest/docs/postman
```

Paste die URL in ein beliebiges AI-Tool (Claude, Cursor, ChatGPT) — es liest die Spec automatisch.

---

## Lizenz

[MIT](LICENSE) — frei verwendbar, auch kommerziell.
