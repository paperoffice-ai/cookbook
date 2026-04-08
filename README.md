# PaperOffice AI Cookbook

Production-ready Recipes for the [PaperOffice AI API](https://paperoffice.ai) — IDP, OCR, PDF, TTS, STT, Translation, DMS, Knowledge Base, MCP and more.

**Copy. Paste. Ship.**

> 38 Recipes · 3 Languages (Bash, Python, Node.js) · All live tested

---

## Quick Start

```bash
# 1. Set API key
export PAPEROFFICE_API_KEY="po_sk_xxx"

# 2. Health Check (no token required)
curl -s "https://api.paperoffice.ai/latest/health" | python3 -m json.tool

# 3. First OCR
curl -X POST "https://api.paperoffice.ai/latest/job/add/paperoffice_aiocr___generate" \
  -H "Authorization: Bearer $PAPEROFFICE_API_KEY" \
  -F "file_1=@document.pdf" -F "ocr_mode=text" -F "priority=900"
```

Or with Python / Node.js:

```bash
pip install requests
python getting-started/first-ocr/example.py document.pdf
```

---

## Recipes

### Getting Started

| Recipe | What it does | Auth |
|---|---|---|
| [Hello World](getting-started/hello-world/) | Health Check — is the API reachable? | VISITOR |
| [First OCR](getting-started/first-ocr/) | Extract text from PDF/image | Bearer |
| [Async Job Polling](getting-started/async-job-polling/) | Submit job → poll → result | Bearer |
| [Webhooks](getting-started/webhooks/) | Receive real-time notifications | Bearer |

### MCP Integration

Native AI tool integration for Cursor, Claude, ChatGPT.

| Setup | Client | URL |
|---|---|---|
| [Cursor Setup](mcp/cursor-setup/) | Cursor IDE | `https://mcp.paperoffice.ai/cursor` |
| [Claude Setup](mcp/claude-setup/) | Claude Desktop / Code | `https://mcp.paperoffice.ai/claude` |
| [ChatGPT Setup](mcp/chatgpt-setup/) | ChatGPT / OpenAI | `https://mcp.paperoffice.ai/openai` |
| [Tool Discovery](mcp/tool-discovery/) | All Clients | `https://mcp.paperoffice.ai/` |

### Document AI — IDP (Intelligent Document Processing)

| Recipe | What it does | Collection |
|---|---|---|
| [Invoice](document-ai/idp/invoice/) | Extract invoice fields (28+ fields) | `invoice` |
| [Custom Fields](document-ai/idp/custom-fields/) | Define custom extraction fields | `idp_fields` |
| [Receipt](document-ai/idp/receipt/) | Read receipt/ticket | `receipt` |
| [Contract](document-ai/idp/contract/) | Contract analysis (parties, duration, value) | `contract` |
| [Identity Document](document-ai/idp/identity-document/) | ID card/passport (name, number, expiry) | `identity` |
| [DATEV Export](document-ai/idp/datev-export/) | IDP results → DATEV accounting entry | `invoice` + CSV |

### Document AI — OCR

| Recipe | What it does | Mode |
|---|---|---|
| [Text Mode](document-ai/ocr/text-mode/) | Plain text, fastest mode | `text` |
| [Complete Mode](document-ai/ocr/complete-mode/) | Text + Bounding Boxes + Tables | `complete` |
| [Searchable PDF](document-ai/ocr/searchable-pdf/) | Create searchable PDF | `text` + `output_searchable_pdf` |

### Document AI — PDF

| Recipe | What it does | Pipeline / Template |
|---|---|---|
| [AI Split](document-ai/pdf/ai-split/) | Intelligently split bulk PDFs | `pdf_ai_split` |
| [Anonymize](document-ai/pdf/anonymize/) | GDPR-compliant PII redaction | `document_anonymize` |
| [Office to PDF](document-ai/pdf/office-to-pdf/) | DOCX/XLSX/PPTX → PDF (native MS Office) | `paperoffice_dataripper___office2pdf` |
| [PDF to Office](document-ai/pdf/pdf-to-office/) | PDF → DOCX/XLSX/PPTX | `paperoffice_dataripper___pdf2office` |

### Document AI — DMS (Headless Document Management)

| Recipe | What it does | Endpoint |
|---|---|---|
| [Workspace Setup](document-ai/dms/workspace-setup/) | Create/manage workspace (tiers, WORM, BYOS) | `/documents/workspace-create` |
| [Document Upload](document-ai/dms/document-upload/) | Upload documents to DMS | `/documents/document-put` |
| [Smart Search](document-ai/dms/smart-search/) | 5 search modes (intelligent, semantic, hybrid, fulltext, RAG) | `/documents/documents-list` |
| [Document Generation](document-ai/dms/document-generation/) | Create PDFs from content or templates | `/document_generation/*` |
| [Document Chat](document-ai/dms/document-chat/) | Chat with a document (RAG) | `/document_intelligence/chat` |

### Analysis AI

| Recipe | What it does | Endpoint |
|---|---|---|
| [Entity Extraction](analysis-ai/entity-extraction/) | Named Entity Recognition (NER) | `/document_intelligence/entities` |
| [Knowledge Graph](analysis-ai/knowledge-graph/) | Build + query knowledge graph | `/knowledge_graph/*` |

### Agent + Media AI

| Recipe | What it does | Endpoint |
|---|---|---|
| [Text-to-Speech](agent-media-ai/tts/) | Text → natural speech (Nadja, etc.) | `/job/add/paperoffice_voice___tts` |
| [Speech-to-Text](agent-media-ai/stt/) | Audio → Text (Transcription) | `/job/add/paperoffice_voice___stt` |
| [Translation](agent-media-ai/translation/) | Text translation (170+ languages) | `/translate/text` |
| [Image Generation](agent-media-ai/image-generation/) | AI image generation with prompt | `/job/add/paperoffice_imagestudio___generate` |

### Knowledge AI

| Recipe | What it does | Endpoint |
|---|---|---|
| [Knowledge Base CRUD](knowledge-ai/knowledge-base-crud/) | Create KB, manage articles | `/knowledge/*` |
| [KB Search](knowledge-ai/kb-search/) | Semantic search in KB | `/knowledge/search` |

### Security + Data AI

| Recipe | What it does | Endpoint |
|---|---|---|
| [Device Fingerprint](security-ai/device-fingerprint/) | Identify, verify, similar + linked devices | `/fingerprint/*` |
| [IP Geolocation](security-ai/ip-geolocation/) | IP → Country, City, ISP, Device | `/ip2location/full` |
| [VAT Validation](security-ai/vat-validation/) | Validate VAT ID + EU tax rates | `/vat/validate` |
| [Fake Email Detection](security-ai/fake-email-detection/) | Detect fake/disposable emails | `/fakeemail/check` |
| [Anonymity Detector](security-ai/anonymity-detector/) | Detect VPN/Proxy/Tor | `/ip2location/vpn` |
| [Geocoding](security-ai/geocoding/) | Address ↔ Coordinates | `/geocoding/*` |
| [Currency Exchange](security-ai/currency-exchange/) | Exchange rates (172 currencies) | `/currency_exchange/get_rates` |
| [Weather](security-ai/weather/) | Weather + forecast + air quality | `/location2weather` |

### AI Prompts

Copy-paste prompts for AI tools.

| Prompt | Tool | Output |
|---|---|---|
| [Claude Invoice Pipeline](ai-prompts/claude-invoice-pipeline.md) | Claude | Batch invoice processing |
| [Cursor MCP Setup](ai-prompts/cursor-mcp-setup.md) | Cursor IDE | MCP configuration |
| [Voice Agent Builder](ai-prompts/voice-agent-builder.md) | Any | Voice Agent (TTS + STT) |
| [Fraud Detection](ai-prompts/fraud-detection-system.md) | Any | Fingerprint + IP Geolocation |
| [Batch PDF Split](ai-prompts/batch-split-3000.md) | Any | Batch PDF splitter |
| [Windsurf Classifier](ai-prompts/windsurf-classifier.md) | Windsurf | Auto-classification |

### Pro Tips

→ [Pro Tips](pro-tips/) — Endpoints, Sync vs Async, Credit System, Retry, MCP, Response Structures

---

## Authentication

**Bearer token required for all job endpoints.**

```bash
export PAPEROFFICE_API_KEY="po_sk_xxx"
```

| Token Type | Prefix | Usage |
|---|---|---|
| System Key | `po_sk_` | Server-to-server, full access |
| User Token | `po_ut_` | User-scoped, depends on license |

> **VISITOR Mode** (no token): Only `GET /health`, `GET /ip2location/*`, `GET /currency_exchange/*`, `GET /vat/rates`. All job/processing endpoints require a Bearer token.

---

## API Endpoints (Overview)

| Endpoint | Purpose |
|---|---|
| `POST /job/add/workflow` | IDP, PDF AI Split, Anonymize |
| `POST /job/add/paperoffice_dataripper___office2pdf` | Office → PDF (native MS Office) |
| `POST /job/add/paperoffice_dataripper___pdf2office` | PDF → Office (DOCX/XLSX/PPTX) |
| `POST /job/add/paperoffice_aiocr___generate` | AI-OCR |
| `POST /job/add/paperoffice_voice___tts` | Text-to-Speech |
| `POST /job/add/paperoffice_voice___stt` | Speech-to-Text |
| `POST /job/add/paperoffice_imagestudio___generate` | Image Generation |
| `POST /translate/text` | Translation |
| `POST /vat/validate` | VAT ID Validation |
| `POST /fakeemail/check` | Fake Email Detection |
| `POST /fingerprint/identify` | Device Fingerprint (v2) |
| `POST /fingerprint/verify` | Device Verification |
| `POST /fingerprint/similar` | Find Similar Devices |
| `POST /geocoding/forward` | Geocoding |
| `POST /ip2location/full` | IP Geolocation |
| `POST /currency_exchange/get_rates` | Exchange Rates |
| `POST /location2weather` | Weather |
| `GET /webhooks/list` | Webhook Management |
| `GET /knowledge/kb_list` | Knowledge Base |
| `POST /documents/documents-list` | DMS Ultimate Search |
| `POST /documents/semantic-search` | DMS Semantic Search |
| `POST /documents/search-hybrid` | DMS Hybrid Search |
| `POST /documents/search-fulltext` | DMS Fulltext Search |
| `POST /documents/rag-search` | DMS RAG Search |
| `POST /documents/ocr-get` | DMS OCR Text Retrieval |
| `POST /document_generation/create-from-content` | Create Document from Content |
| `POST /document_generation/create-from-template` | Create Document from Template |

---

## API Documentation

Complete Postman Collection:

```
https://api.paperoffice.ai/latest/docs/postman
```

Paste the URL into any AI tool (Claude, Cursor, ChatGPT) — it reads the spec automatically.

---

## License

[MIT](LICENSE) — free to use, including commercially.
