# PaperOffice AI Cookbook

### The AI-Native Developer Toolkit for Document Intelligence

> **MCP-First · API-First · Vibe Coding First**
>
> 300+ API/MCP tools · 38 Recipes · 8 AI Prompts · 4 MCP Configs

[![Smithery badge](https://img.shields.io/badge/Smithery-document--operations-7c3aed)](https://smithery.ai/servers/paperoffice/document-operations)

---

## Start in 30 Seconds

Forget reading docs. Paste one URL into your AI IDE and start building:

```
https://api.paperoffice.ai/latest/docs/llms.txt
```

**That's it.** `llms.txt` is the machine-readable API guide — 300+ tools, auth, Start-SLA lanes, response envelopes. Your AI reads it and generates production code for you. The live [Postman collection](https://api.paperoffice.ai/latest/docs/postman) carries the full request/response samples when your AI needs a specific endpoint in detail.

### Try it now

Open **Cursor**, **Claude**, **ChatGPT**, or **Windsurf** and paste:

```
Read this API guide first, completely:
https://api.paperoffice.ai/latest/docs/llms.txt

Extract all fields from this invoice PDF using IDP.
Use model=premium and processing_lane=instant for instant results.
Read the API key from the environment variable PAPEROFFICE_API_KEY.
```

Your AI generates a working script. No docs to read. No boilerplate to write.

---

## Before You Start

Three steps, about two minutes, no credit card.

| Step | What to do | Where |
|------|-----------|-------|
| 1 · Account | Create a free PaperOffice account. The free plan is meant for trying things out; plan scope and credit prices are on the [pricing page](https://paperoffice.ai/en/pricing/). | [app.paperoffice.ai/en/register/](https://app.paperoffice.ai/en/register/) |
| 2 · Token | Sign in, open **Account → API** and create a **User token** (`po_ut_…`). You can show and copy it again there at any time, rotate it, or set a credit budget per token. | [app.paperoffice.ai](https://app.paperoffice.ai) → Account → API |
| 3 · Environment | `cp .env.example .env`, paste the token into `PAPEROFFICE_API_KEY`. Every recipe and every MCP config in this repo reads that variable. | this repo |

**What every call costs.** Processing endpoints consume credits from your plan; the `processing_lane` you choose sets the factor (`no_sla` ×1 … `instant` ×5). Rejected requests cost nothing. With a token, every billable call costs at least 5 credits; `GET /health`, job polling (`GET /job/get`), `/billing/*` reads and `/docs/*` are always free. Without a token, the VISITOR endpoints listed under [Authentication](#authentication) are free and rate-limited. Details: [Pro Tips → Credit System](pro-tips/#credit-system).

**Which token for what.** A User token sees everything your account sees. A Group token (`po_gt_…`) is limited to the workspaces of one group — use it for a team, a customer, or a reviewer. Both work for REST and MCP. System keys (`po_sk_`) are REST-only and the MCP server rejects them; publishable keys (`po_pk_`) are for browser widgets only.

**Using an AI client instead of code?** Claude, ChatGPT and Grok sign in with OAuth — no token to paste. Cursor and Windsurf take the token as a plugin variable. See [MCP Integration](#-mcp-integration--ai-native-access) below.

**Stuck?** [Help & FAQ](https://help.paperoffice.ai/) · [Support](https://paperoffice.ai/en/support/) · [GitHub Issues](https://github.com/paperoffice-ai/cookbook/issues) for anything wrong in this repo.

---

## 🔗 MCP Integration — AI-Native Access

Connect your AI IDE **directly** to PaperOffice. The Documents Operations catalog becomes native AI actions — no REST calls, no boilerplate, no context switching. Auth: OAuth 2.1 (Claude, ChatGPT, Grok) or a user/group token (`po_ut_` / `po_gt_`); `po_sk_` and `po_pk_` are rejected by the MCP server.

### One-Click Setup

<details>
<summary><strong>Cursor IDE</strong> — <code>.cursor/mcp.json</code></summary>

```json
{
  "mcpServers": {
    "paperoffice": {
      "url": "https://mcp.paperoffice.ai/cursor",
      "headers": {
        "Authorization": "Bearer po_ut_..."
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
      "url": "https://mcp.paperoffice.ai/claude"
    }
  }
}
```

Claude signs in with OAuth 2.1 on the first request — no token in the file.

→ [Full Claude Setup Guide](mcp/claude-setup/)

</details>

<details>
<summary><strong>ChatGPT</strong> — Settings → Connectors</summary>

Paste `https://mcp.paperoffice.ai/chatgpt` and complete the OAuth sign-in. No token in a file.

→ [Full ChatGPT Setup Guide](mcp/chatgpt-setup/)

</details>

<details>
<summary><strong>Windsurf / Other MCP Clients</strong></summary>

```json
{
  "mcpServers": {
    "paperoffice": {
      "url": "https://mcp.paperoffice.ai/dms",
      "headers": {
        "Authorization": "Bearer po_ut_..."
      }
    }
  }
}
```

`/dms` is the canonical Documents Operations URL (same catalog as `/cursor`). For media, CRM and telephony use `/mcp-full`.

</details>

### All MCP Endpoints

| Client | URL |
|--------|-----|
| Cursor / Windsurf | `https://mcp.paperoffice.ai/cursor` |
| Claude Desktop / Anthropic Directory | `https://mcp.paperoffice.ai/claude` |
| ChatGPT | `https://mcp.paperoffice.ai/chatgpt` |
| Grok | `https://mcp.paperoffice.ai/grok` |
| [Smithery](https://smithery.ai/servers/paperoffice/document-operations) | `https://mcp.paperoffice.ai/smithery` |
| Headless DMS (canonical) | `https://mcp.paperoffice.ai/dms` |
| Everything, all modules | `https://mcp.paperoffice.ai/mcp-full` |

→ [Tool Discovery Guide](mcp/tool-discovery/) — `tools/list` shows the core; `po_mcp_tools_search` reaches the rest of the 300+ catalog

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
| [Workspace Setup](document-ai/dms/workspace-setup/) | Create/manage workspace (tiers, WORM, BYOS) | `/documents/workspaces-create` |
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
| [Weather](security-ai/weather/) | Weather + forecast + air quality | `/weather` |

### Pro Tips

→ [Pro Tips](pro-tips/) — Sync vs Async, Credit System, Response Structures, Retry Strategy, Parameter Reference

---

## Authentication

**Bearer token required for all job endpoints.** Create tokens at [app.paperoffice.ai](https://app.paperoffice.ai) → *Account → API*.

```bash
export PAPEROFFICE_API_KEY="po_ut_xxx"
```

| Token Type | Prefix | REST API | MCP |
|------------|--------|----------|-----|
| User Token | `po_ut_` | yes | yes |
| Group Token | `po_gt_` | yes — limited to the group's workspaces | yes |
| System Key | `po_sk_` | yes — server-to-server, full account | **rejected** |
| Publishable Key | `po_pk_` | browser widgets only | **rejected** |

> **VISITOR Mode** (no token): Only `GET /health`, `POST /ip2location/*`, `POST /currency_exchange/get_rates`, `GET /vat/rates` (rate-limited). All other endpoints require Bearer token.

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
| `GET /weather` | Weather |
| `GET /webhooks/list` | Webhook Management |
| `POST /webhooks/subscribe` | Register Webhook |
| `GET /knowledge/kb_list` | Knowledge Base List |
| `POST /knowledge/search` | KB Search |
| `POST /documents/documents-list` | DMS Search |
| `POST /documents/document-search` | Semantic / Hybrid / Fulltext / RAG Search |
| `POST /documents/document-put` | DMS Upload |
| `POST /documents/workspaces-create` | Create Workspace |
| `GET /documents/workspaces-list` | List Workspaces |
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

## Support

| Question about … | Go to |
|------------------|-------|
| Using the API or the app, billing, account | [Help & FAQ](https://help.paperoffice.ai/) · [Support](https://paperoffice.ai/en/support/) |
| A recipe in this repo that does not work | [GitHub Issues](https://github.com/paperoffice-ai/cookbook/issues) — include the endpoint, the `processing_lane`, and the `error_code` from the response |
| MCP setup for Claude, ChatGPT, Cursor, Grok | [MCP documentation](https://paperoffice.ai/en/developer/mcp/) · [paperoffice-mcp-setup](https://github.com/paperoffice-ai/paperoffice-mcp-setup) |
| Teaching an agent the procedures (not just the tools) | [paperoffice-skills](https://github.com/paperoffice-ai/paperoffice-skills) — Agent Skills for Claude Code, claude.ai and Cursor |
| Reseller or integration partnership | [Partner program](https://paperoffice.ai/en/partner/) |

Typical error codes: `401 NOT_AUTHENTICATED` → no Bearer header sent · `401 TOKEN_NOT_FOUND` → token wrong, revoked, or pasted with a typo · `403 GROUP_RESTRICTION` → the group behind your token lacks that module (use a User token or ask the account owner) · `403 WORKSPACE_ACCESS_DENIED` → the workspace belongs to another group · `402 INSUFFICIENT_CREDITS` → the account is out of credits, top up or use a cheaper `processing_lane` · `402 BUDGET_EXHAUSTED` → this token's own credit budget is reached, raise it under Account → API. The full table is in [llms.txt](https://api.paperoffice.ai/latest/docs/llms.txt).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) — we follow the **Vibe Coding First** philosophy.

## License

[MIT](LICENSE) — free to use, including commercially.
