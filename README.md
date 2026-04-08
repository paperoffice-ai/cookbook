# PaperOffice AI Cookbook

Production-ready Recipes für die [PaperOffice AI API](https://paperoffice.ai) — IDP, OCR, PDF, TTS, STT, Translation, DMS, Knowledge Base, MCP und mehr.

**Copy. Paste. Ship.**

> 44 Recipes · 3 Sprachen (Bash, Python, Node.js) · Alle live getestet

---

## Quick Start

```bash
# 1. API-Key setzen
export PAPEROFFICE_API_KEY="po_sk_xxx"

# 2. Health Check (kein Token nötig)
curl -s "https://api.paperoffice.ai/latest/health" | python3 -m json.tool

# 3. Erstes OCR
curl -X POST "https://api.paperoffice.ai/latest/job/add/paperoffice_aiocr___generate" \
  -H "Authorization: Bearer $PAPEROFFICE_API_KEY" \
  -F "file_1=@dokument.pdf" -F "ocr_mode=text" -F "priority=900"
```

Oder mit Python / Node.js:

```bash
pip install requests
python getting-started/first-ocr/example.py dokument.pdf
```

---

## Recipes

### Getting Started

| Recipe | Was es tut | Auth |
|---|---|---|
| [Hello World](getting-started/hello-world/) | Health Check — API erreichbar? | VISITOR |
| [First OCR](getting-started/first-ocr/) | Text aus PDF/Bild extrahieren | Bearer |
| [Async Job Polling](getting-started/async-job-polling/) | Job einreichen → pollen → Ergebnis | Bearer |
| [Webhooks](getting-started/webhooks/) | Echtzeit-Benachrichtigungen empfangen | Bearer |

### MCP Integration

Native AI-Tool-Integration für Cursor, Claude, ChatGPT.

| Setup | Client | URL |
|---|---|---|
| [Cursor Setup](mcp/cursor-setup/) | Cursor IDE | `https://mcp.paperoffice.ai/cursor` |
| [Claude Setup](mcp/claude-setup/) | Claude Desktop / Code | `https://mcp.paperoffice.ai/claude` |
| [ChatGPT Setup](mcp/chatgpt-setup/) | ChatGPT / OpenAI | `https://mcp.paperoffice.ai/openai` |
| [Tool Discovery](mcp/tool-discovery/) | Alle Clients | `https://mcp.paperoffice.ai/` |

### Document AI — IDP (Intelligent Document Processing)

| Recipe | Was es tut | Collection |
|---|---|---|
| [Invoice](document-ai/idp/invoice/) | Rechnungsfelder extrahieren (28+ Felder) | `invoice` |
| [Custom Fields](document-ai/idp/custom-fields/) | Eigene Extraktionsfelder definieren | `idp_fields` |
| [Receipt](document-ai/idp/receipt/) | Kassenbon/Quittung auslesen | `receipt` |
| [Contract](document-ai/idp/contract/) | Vertragsanalyse (Parteien, Laufzeit, Wert) | `contract` |
| [Identity Document](document-ai/idp/identity-document/) | Ausweis/Pass (Name, Nummer, Ablauf) | `identity` |
| [DATEV Export](document-ai/idp/datev-export/) | IDP-Ergebnisse → DATEV-Buchungssatz | `invoice` + CSV |

### Document AI — OCR

| Recipe | Was es tut | Modus |
|---|---|---|
| [Text Mode](document-ai/ocr/text-mode/) | Reiner Text, schnellster Modus | `text` |
| [Complete Mode](document-ai/ocr/complete-mode/) | Text + Bounding Boxes + Tabellen | `complete` |
| [Searchable PDF](document-ai/ocr/searchable-pdf/) | Durchsuchbare PDF erstellen | `text` + `output_searchable_pdf` |

### Document AI — PDF

| Recipe | Was es tut | Template |
|---|---|---|
| [AI Split](document-ai/pdf/ai-split/) | Sammel-PDFs intelligent splitten | `pdf_ai_split` |
| [Merge](document-ai/pdf/merge/) | Mehrere PDFs zusammenfügen | `pdf_merge` |
| [Convert](document-ai/pdf/convert/) | PDF → DOCX, XLSX, HTML, etc. | `pdf_convert` |
| [Anonymize](document-ai/pdf/anonymize/) | DSGVO-konforme PII-Schwärzung | `pdf_anonymize` |

### Document AI — DMS (Headless Document Management)

| Recipe | Was es tut | Endpoint |
|---|---|---|
| [Workspace Setup](document-ai/dms/workspace-setup/) | Workspace erstellen/verwalten | `/documents/workspace_*` |
| [Document Upload](document-ai/dms/document-upload/) | Dokumente hochladen + taggen | `/documents/upload` |
| [Smart Search](document-ai/dms/smart-search/) | Semantische Dokumentensuche | `/documents/search` |
| [Document Generation](document-ai/dms/document-generation/) | KI-basierte Dokumentenerstellung | `/document_generation/generate` |
| [Document Chat](document-ai/dms/document-chat/) | Chat mit einem Dokument (RAG) | `/document_intelligence/chat` |

### Analysis AI

| Recipe | Was es tut | Endpoint |
|---|---|---|
| [Entity Extraction](analysis-ai/entity-extraction/) | Named Entity Recognition (NER) | `/document_intelligence/entities` |
| [Knowledge Graph](analysis-ai/knowledge-graph/) | Wissensgraph aufbauen + abfragen | `/knowledge_graph/*` |

### Agent + Media AI

| Recipe | Was es tut | Endpoint |
|---|---|---|
| [Text-to-Speech](agent-media-ai/tts/) | Text → natürliche Sprache (Nadja, etc.) | `/job/add/paperoffice_voice___tts` |
| [Speech-to-Text](agent-media-ai/stt/) | Audio → Text (Transkription) | `/job/add/paperoffice_voice___stt` |
| [Translation](agent-media-ai/translation/) | Textübersetzung (170+ Sprachen) | `/translate/text` |
| [Image Generation](agent-media-ai/image-generation/) | KI-Bildgenerierung mit Prompt | `/job/add/paperoffice_imagestudio___generate` |

### Knowledge AI

| Recipe | Was es tut | Endpoint |
|---|---|---|
| [Knowledge Base CRUD](knowledge-ai/knowledge-base-crud/) | KB erstellen, Artikel verwalten | `/knowledge/*` |
| [KB Search](knowledge-ai/kb-search/) | Semantische Suche in der KB | `/knowledge/search` |

### Security + Data AI

| Recipe | Was es tut | Endpoint |
|---|---|---|
| [Device Fingerprint](security-ai/device-fingerprint/) | Gerät verifizieren | `/fingerprint/verify` |
| [IP Geolocation](security-ai/ip-geolocation/) | IP → Land, Stadt, ISP, Device | `/ip2location/full` |
| [VAT Validation](security-ai/vat-validation/) | USt-ID prüfen + EU-Steuersätze | `/vat/validate` |
| [Fake Email Detection](security-ai/fake-email-detection/) | Fake/Disposable-E-Mails erkennen | `/fakeemail/check` |
| [Anonymity Detector](security-ai/anonymity-detector/) | VPN/Proxy/Tor erkennen | `/ip2location/vpn` |
| [Geocoding](security-ai/geocoding/) | Adresse ↔ Koordinaten | `/geocoding/*` |
| [Currency Exchange](security-ai/currency-exchange/) | Wechselkurse (172 Währungen) | `/currency_exchange/get_rates` |
| [Weather](security-ai/weather/) | Wetter + Vorhersage + Luftqualität | `/location2weather` |

### AI Prompts

Copy-Paste Prompts für AI-Tools.

| Prompt | Tool | Output |
|---|---|---|
| [Claude Invoice Pipeline](ai-prompts/claude-invoice-pipeline.md) | Claude | Batch-Rechnungsverarbeitung |
| [Cursor MCP Setup](ai-prompts/cursor-mcp-setup.md) | Cursor IDE | MCP-Konfiguration |
| [Voice Agent Builder](ai-prompts/voice-agent-builder.md) | Beliebig | Voice Agent (TTS + STT) |
| [Fraud Detection](ai-prompts/fraud-detection-system.md) | Beliebig | Fingerprint + IP Geolocation |
| [Batch PDF Split](ai-prompts/batch-split-3000.md) | Beliebig | Batch-PDF-Splitter |
| [Windsurf Classifier](ai-prompts/windsurf-classifier.md) | Windsurf | Auto-Klassifizierung |

### Pro Tips

→ [Pro Tips](pro-tips/) — Endpoints, Sync vs Async, Credit-System, Retry, MCP, Response-Strukturen

---

## Authentifizierung

**Bearer Token für alle Job-Endpoints erforderlich.**

```bash
export PAPEROFFICE_API_KEY="po_sk_xxx"
```

| Token-Typ | Prefix | Verwendung |
|---|---|---|
| System Key | `po_sk_` | Server-to-Server, voller Zugriff |
| User Token | `po_ut_` | User-scoped, abhängig von Lizenz |

> **VISITOR-Mode** (kein Token): Nur `GET /health`, `GET /ip2location/*`, `GET /currency_exchange/*`, `GET /vat/rates`. Alle Job/Processing-Endpoints benötigen einen Bearer Token.

---

## API-Endpoints (Übersicht)

| Endpoint | Zweck |
|---|---|
| `POST /job/add/workflow` | IDP, PDF Split/Merge/Convert/Anonymize |
| `POST /job/add/paperoffice_aiocr___generate` | AI-OCR |
| `POST /job/add/paperoffice_voice___tts` | Text-to-Speech |
| `POST /job/add/paperoffice_voice___stt` | Speech-to-Text |
| `POST /job/add/paperoffice_imagestudio___generate` | Bildgenerierung |
| `POST /translate/text` | Übersetzung |
| `POST /vat/validate` | USt-ID Prüfung |
| `POST /fakeemail/check` | Fake-Email-Erkennung |
| `POST /fingerprint/verify` | Device Fingerprint |
| `POST /geocoding/forward` | Geocoding |
| `POST /ip2location/full` | IP Geolocation |
| `POST /currency_exchange/get_rates` | Wechselkurse |
| `POST /location2weather` | Wetter |
| `GET /webhooks/list` | Webhook-Verwaltung |
| `GET /knowledge/kb_list` | Knowledge Base |
| `POST /documents/search` | DMS-Suche |

---

## API-Dokumentation

Vollständige Postman Collection:

```
https://api.paperoffice.ai/latest/docs/postman
```

Paste die URL in ein beliebiges AI-Tool (Claude, Cursor, ChatGPT) — es liest die Spec automatisch.

---

## Lizenz

[MIT](LICENSE) — frei verwendbar, auch kommerziell.
