# PaperOffice AI Cookbook

### The AI-Native Developer Toolkit for Document Intelligence

> **MCP-First · API-First · Vibe Coding First**
>
> 409 AI Tools · 38 Recipes · 6 AI Prompts · 5 MCP Configs

---

## Start in 30 Seconds

Forget reading docs. Paste one URL into your AI IDE and start building:

```
https://api.paperoffice.ai/latest/docs/postman
```

**That's it.** Your AI reads the entire API spec — 409 tools, all parameters, all response formats — and generates production code for you.

### Try it now

Open **Cursor**, **Claude**, **ChatGPT**, or **Windsurf** and paste:

```
Read this API documentation:
https://api.paperoffice.ai/latest/docs/postman

Extract all fields from this invoice PDF using IDP.
Use model=premium and priority=900 for instant results.
```

Your AI generates a working script. No docs to read. No boilerplate to write.

---

## 🔗 MCP Integration — AI-Native Access

Connect your AI IDE **directly** to PaperOffice. All 409 tools become native AI actions — no REST calls, no boilerplate, no context switching.

### One-Click Setup

<details>
<summary><strong>Cursor IDE</strong> — <code>.cursor/mcp.json</code></summary>

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

→ [Full Cursor Setup Guide](mcp/cursor-setup/)

</details>

<details>
<summary><strong>Claude Desktop / Claude Code</strong> — <code>claude_desktop_config.json</code></summary>

```json
{
  "mcpServers": {
    "paperoffice": {
      "url": "https://mcp.paperoffice.ai/claude",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      }
    }
  }
}
```

→ [Full Claude Setup Guide](mcp/claude-setup/)

</details>

<details>
<summary><strong>ChatGPT / OpenAI</strong></summary>

```json
{
  "mcpServers": {
    "paperoffice": {
      "url": "https://mcp.paperoffice.ai/openai",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      }
    }
  }
}
```

→ [Full ChatGPT Setup Guide](mcp/chatgpt-setup/)

</details>

<details>
<summary><strong>Windsurf / Other MCP Clients</strong></summary>

```json
{
  "mcpServers": {
    "paperoffice": {
      "url": "https://mcp.paperoffice.ai/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      }
    }
  }
}
```

</details>

### All MCP Endpoints

| Client | URL |
|--------|-----|
| Cursor IDE | `https://mcp.paperoffice.ai/cursor` |
| Claude Desktop / Code | `https://mcp.paperoffice.ai/claude` |
| ChatGPT / OpenAI | `https://mcp.paperoffice.ai/openai` |
| Standard MCP | `https://mcp.paperoffice.ai/mcp` |
| Universal | `https://mcp.paperoffice.ai/` |

→ [Tool Discovery Guide](mcp/tool-discovery/) — explore all 409 tools via `tools/list`

---

## 🤖 AI Prompts — Copy, Paste, Ship

Ready-to-paste prompts for the most common workflows. Open your AI tool, paste the prompt, get production code.

| Prompt | Tool | What you get |
|--------|------|-------------|
| [Invoice Processing Pipeline](ai-prompts/claude-invoice-pipeline.md) | Claude | Batch invoice extraction → CSV with bounding box verification |
| [Cursor MCP Setup](ai-prompts/cursor-mcp-setup.md) | Cursor | Complete MCP config + IDE-native Document AI |
| [Voice Agent Builder](ai-prompts/voice-agent-builder.md) | Any | TTS + STT voice agent with natural speech |
| [Fraud Detection System](ai-prompts/fraud-detection-system.md) | Any | Device Fingerprint + IP Geolocation risk scoring |
| [Batch PDF Splitter (3000 pages)](ai-prompts/batch-split-3000.md) | Any | AI-powered bulk PDF splitting with smart filenames |
| [Auto-Classification System](ai-prompts/windsurf-classifier.md) | Windsurf | Folder watcher → OCR → classify → sort documents |
| [DMS Upload + Search Pipeline](ai-prompts/dms-pipeline.md) | Any | Upload documents → Workspace → Smart Search |
| [OCR Data Extraction](ai-prompts/ocr-data-extraction.md) | Any | Extract tables + structured data from scanned documents |

### How AI Prompts Work

Every prompt starts with:

```
Read this API documentation:
https://api.paperoffice.ai/latest/docs/postman
```

This gives the AI **full context** about all endpoints, parameters, and response formats. The AI then generates the complete solution — no manual coding needed.

---

## 📚 Recipes — Code Reference

Traditional code examples in **Bash**, **Python**, and **Node.js** for every API capability. Use these as reference when you need to understand the exact API contract.

### Getting Started

| Recipe | What it does | Auth |
|--------|-------------|------|
| [Hello World](getting-started/hello-world/) | Health Check — is the API reachable? | VISITOR |
| [First OCR](getting-started/first-ocr/) | Extract text from PDF/image | Bearer |
| [Async Job Polling](getting-started/async-job-polling/) | Submit job → poll → download result | Bearer |
| [Webhooks](getting-started/webhooks/) | Receive real-time notifications | Bearer |

### Document AI — IDP (Intelligent Document Processing)

| Recipe | What it does | Collection |
|--------|-------------|-----------|
| [Invoice](document-ai/idp/invoice/) | Extract invoice fields (28+ fields) | `invoice` |
| [Custom Fields](document-ai/idp/custom-fields/) | Define custom extraction fields | `idp_fields` |
| [Receipt](document-ai/idp/receipt/) | Read receipt/ticket | `receipt` |
| [Contract](document-ai/idp/contract/) | Contract analysis (parties, duration, value) | `legal_document` |
| [Identity Document](document-ai/idp/identity-document/) | ID card/passport (name, number, expiry) | `identity_document` |
| [DATEV Export](document-ai/idp/datev-export/) | IDP results → DATEV accounting entry | `invoice` + CSV |

### Document AI — OCR

| Recipe | What it does | Mode |
|--------|-------------|------|
| [Text Mode](document-ai/ocr/text-mode/) | Plain text, fastest mode | `text` |
| [Complete Mode](document-ai/ocr/complete-mode/) | Text + Bounding Boxes + Tables + Layout | `complete` |
| [Searchable PDF](document-ai/ocr/searchable-pdf/) | Create searchable PDF from scans | `text` + `output_searchable_pdf` |

### Document AI — PDF

| Recipe | What it does | Pipeline |
|--------|-------------|---------|
| [AI Split](document-ai/pdf/ai-split/) | Intelligently split bulk PDFs | `pdf_ai_split` |
| [Anonymize](document-ai/pdf/anonymize/) | GDPR-compliant PII redaction (2-step) | `document_anonymize` |
| [Office to PDF](document-ai/pdf/office-to-pdf/) | DOCX/XLSX/PPTX → PDF (native MS Office) | `paperoffice_dataripper___office2pdf` |
| [PDF to Office](document-ai/pdf/pdf-to-office/) | PDF → DOCX/XLSX/PPTX | `paperoffice_dataripper___pdf2office` |

### Document AI — DMS (Headless Document Management)

| Recipe | What it does | Endpoint |
|--------|-------------|---------|
| [Workspace Setup](document-ai/dms/workspace-setup/) | Create/manage workspace (tiers, WORM, BYOS) | `/documents/workspace-create` |
| [Document Upload](document-ai/dms/document-upload/) | Upload documents to DMS | `/documents/document-put` |
| [Smart Search](document-ai/dms/smart-search/) | 5 search modes (intelligent, semantic, hybrid, fulltext, RAG) | `/documents/document-search` |
| [Document Generation](document-ai/dms/document-generation/) | Create PDFs from content or templates | `/document_generation/*` |
| [Document Chat](document-ai/dms/document-chat/) | Chat with a document (GraphRAG) | `/knowledge_graph/universe` |

### Analysis AI

| Recipe | What it does | Endpoint |
|--------|-------------|---------|
| [Entity Extraction](analysis-ai/entity-extraction/) | Named Entity Recognition (NER) | `/document_intelligence/entities` |
| [Knowledge Graph](analysis-ai/knowledge-graph/) | Query + visualize knowledge graph (GraphRAG) | `/knowledge_graph/universe` |

### Agent + Media AI

| Recipe | What it does | Endpoint |
|--------|-------------|---------|
| [Text-to-Speech](agent-media-ai/tts/) | Text → natural speech (50+ voices) | `/job/add/paperoffice_voice___tts` |
| [Speech-to-Text](agent-media-ai/stt/) | Audio → text (transcription) | `/job/add/paperoffice_voice___stt` |
| [Translation](agent-media-ai/translation/) | Text translation (170+ languages) | `/translate/text` |
| [Image Generation](agent-media-ai/image-generation/) | AI image generation + background removal | `/job/add/paperoffice_imagestudio___generate` |

### Knowledge AI

| Recipe | What it does | Endpoint |
|--------|-------------|---------|
| [Knowledge Base CRUD](knowledge-ai/knowledge-base-crud/) | Create KB, manage articles | `/knowledge/*` |
| [KB Search](knowledge-ai/kb-search/) | Semantic search in Knowledge Base | `/knowledge/search` |

### Security + Data AI

| Recipe | What it does | Endpoint |
|--------|-------------|---------|
| [Device Fingerprint](security-ai/device-fingerprint/) | Identify, verify, similar + linked devices | `/fingerprint/*` |
| [IP Geolocation](security-ai/ip-geolocation/) | IP → Country, City, ISP, Device | `/ip2location/full` |
| [VAT Validation](security-ai/vat-validation/) | Validate VAT ID + EU tax rates | `/vat/validate` |
| [Fake Email Detection](security-ai/fake-email-detection/) | Detect fake/disposable emails | `/fakeemail/check` |
| [Anonymity Detector](security-ai/anonymity-detector/) | Detect VPN/Proxy/Tor | `/ip2location/vpn` |
| [Geocoding](security-ai/geocoding/) | Address ↔ Coordinates | `/geocoding/*` |
| [Currency Exchange](security-ai/currency-exchange/) | Exchange rates (172 currencies) | `/currency_exchange/get_rates` |
| [Weather](security-ai/weather/) | Weather + forecast + air quality | `/location2weather` |

### Pro Tips

→ [Pro Tips](pro-tips/) — Sync vs Async, Credit System, Response Structures, Retry Strategy, Parameter Reference

---

## Authentication

**Bearer token required for all job endpoints.**

```bash
export PAPEROFFICE_API_KEY="po_sk_xxx"
```

| Token Type | Prefix | Usage |
|------------|--------|-------|
| System Key | `po_sk_` | Server-to-server, full access |
| User Token | `po_ut_` | User-scoped, depends on license |

> **VISITOR Mode** (no token): Only `GET /health`, `GET /ip2location/*`, `GET /currency_exchange/*`, `GET /vat/rates`. All other endpoints require Bearer token.

---

## API Endpoints (Full Reference)

<details>
<summary>Click to expand — all endpoints at a glance</summary>

### Job-based Endpoints (File Processing)

| Pipeline | Purpose |
|----------|---------|
| `POST /job/add/workflow` | IDP, PDF AI Split, Anonymize |
| `POST /job/add/paperoffice_aiocr___generate` | AI-OCR |
| `POST /job/add/paperoffice_voice___tts` | Text-to-Speech |
| `POST /job/add/paperoffice_voice___stt` | Speech-to-Text |
| `POST /job/add/paperoffice_imagestudio___generate` | Image Generation |
| `POST /job/add/paperoffice_imagestudio___remove_bg` | Background Removal |
| `POST /job/add/paperoffice_dataripper___office2pdf` | Office → PDF |
| `POST /job/add/paperoffice_dataripper___pdf2office` | PDF → Office |

### Dedicated REST Endpoints

| Endpoint | Purpose |
|----------|---------|
| `POST /translate/text` | Translation |
| `GET /translate/languages` | Language List |
| `POST /vat/validate` | VAT ID Validation |
| `GET /vat/rates` | EU Tax Rates |
| `POST /fakeemail/check` | Fake Email Detection |
| `POST /fingerprint/identify` | Device Fingerprint (v2) |
| `POST /fingerprint/verify` | Device Verification |
| `POST /fingerprint/similar` | Find Similar Devices |
| `POST /geocoding/forward` | Address → Coordinates |
| `POST /geocoding/reverse` | Coordinates → Address |
| `POST /ip2location/full` | IP Geolocation |
| `POST /ip2location/vpn` | VPN/Proxy Detection |
| `POST /currency_exchange/get_rates` | Exchange Rates |
| `POST /location2weather` | Weather |
| `GET /webhooks/list` | Webhook Management |
| `POST /webhooks/subscribe` | Register Webhook |
| `GET /knowledge/kb_list` | Knowledge Base List |
| `POST /knowledge/search` | KB Search |
| `POST /documents/documents-list` | DMS Search |
| `POST /documents/document-search` | Semantic / Hybrid / Fulltext / RAG Search |
| `POST /documents/document-put` | DMS Upload |
| `POST /documents/workspace-create` | Create Workspace |
| `POST /document_generation/create-from-content` | Document from Content |
| `POST /document_generation/create-from-template` | Document from Template |
| `POST /knowledge_graph/universe` | GraphRAG Q&A |
| `GET /job/get/{job_id}` | Job Status |
| `GET /job/download/{token}` | Download Result |
| `GET /health` | Health Check |
| `GET /voices_info` | TTS Voice List |

</details>

---

## Postman Collection

The canonical API reference — always up to date, dynamically generated:

```
https://api.paperoffice.ai/latest/docs/postman
```

Import into Postman, or paste into any AI tool for full context.

---

## Project Setup

```bash
# Clone
git clone https://github.com/paperoffice-ai/cookbook.git
cd cookbook

# Environment
cp .env.example .env
# Edit .env with your API key

# Python dependencies
pip install -r requirements.txt

# Run any recipe
bash getting-started/hello-world/example.sh
python getting-started/first-ocr/example.py document.pdf
node getting-started/first-ocr/example.js document.pdf
```

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) — we follow the **Vibe Coding First** philosophy.

## License

[MIT](LICENSE) — free to use, including commercially.
